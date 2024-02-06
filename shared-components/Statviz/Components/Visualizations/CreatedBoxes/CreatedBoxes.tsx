import { Card, CardBody } from "@chakra-ui/react";
import { useMemo } from "react";
import {
  filter,
  sum,
  summarize,
  tidy,
  groupBy,
  complete,
  fullSeqDateISOString,
  map,
} from "@tidyjs/tidy";
import { format, getISOWeek, getYear } from "date-fns";
import BarChart from "../../Nivo-graphs/BarChart";
import { BoxesOrItemsCount } from "../../../Dashboard/ItemsAndBoxes";
import VisHeader from "../../VisHeader";
import NoDataCard from "../../NoDataCard";
import getOnExport from "../../../utils/chartExport";
import { CreatedBoxesData, CreatedBoxesResult } from "../../../../types/generated/graphql";

const visId = "created-boxes";

interface ICreatedBoxesProps {
  width: string;
  height: string;
  data: CreatedBoxesData;
  boxesOrItems: BoxesOrItemsCount;
}

export default function CreatedBoxes({ width, height, data, boxesOrItems }: ICreatedBoxesProps) {
  const onExport = getOnExport(BarChart);
  const facts = data.facts as CreatedBoxesResult[];

  const getChartData = () => {
    const createdBoxes = tidy(
      facts,
      filter((row) => row.createdOn !== null),
      groupBy("createdOn", [
        summarize({
          itemsCount: sum("itemsCount"),
          boxesCount: sum("boxesCount"),
        }),
      ]),
      map((row) => ({
        ...row,
        createdOn: new Date(`${row.createdOn}Z`).toISOString(),
      })),
      complete<{ createdOn: string; boxesCount: number; itemsCount: number }>(
        // fill days without new boxes
        {
          createdOn: fullSeqDateISOString("createdOn", "day", 1),
        },
        { boxesCount: 0, itemsCount: 0 },
      ),
      map((row) => ({
        ...row,
        createdOn: new Date(row.createdOn),
      })),
    );

    const LIMIT_GROUP_BY_DAYS = 29;
    const LIMIT_GROUP_BY_WEEK = 197;
    const LIMIT_GROUP_BY_MONTH = 10960;
    if (createdBoxes.length < LIMIT_GROUP_BY_DAYS) {
      return tidy(
        createdBoxes,
        map((row) => ({
          ...row,
          createdOn: format(new Date(row.createdOn), "dd LLL yyyy"),
        })),
      );
    }
    if (createdBoxes.length < LIMIT_GROUP_BY_WEEK) {
      // group by week
      return tidy(
        createdBoxes,
        map((row) => ({
          ...row,
          createdOn: `week ${getISOWeek(row.createdOn)} in ${getYear(row.createdOn)} `,
        })),
        groupBy("createdOn", [
          summarize({
            itemsCount: sum("itemsCount"),
            boxesCount: sum("boxesCount"),
          }),
        ]),
      );
    }
    if (createdBoxes.length < LIMIT_GROUP_BY_MONTH) {
      // group by month
      return tidy(
        createdBoxes,
        map((row) => ({
          ...row,
          createdOn: `${row.createdOn.toLocaleString("default", {
            month: "short",
          })} ${getYear(row.createdOn)}`,
        })),
        groupBy("createdOn", [
          summarize({
            itemsCount: sum("itemsCount"),
            boxesCount: sum("boxesCount"),
          }),
        ]),
      );
    }
    // group by year
    return tidy(
      createdBoxes,
      map((row) => ({
        ...row,
        createdOn: `${getYear(row.createdOn)}`,
      })),
      groupBy("createdOn", [
        summarize({
          itemsCount: sum("itemsCount"),
          boxesCount: sum("boxesCount"),
        }),
      ]),
    );
  };

  // should only execute if data changes
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const createdBoxesPerDay = useMemo(getChartData, [data]);

  const heading = boxesOrItems === "itemsCount" ? "New Items" : "Created Boxes";

  if (createdBoxesPerDay.length === 0) {
    return <NoDataCard header={heading} />;
  }

  const chartProps = {
    visId: "preview-created-boxes",
    data: createdBoxesPerDay,
    indexBy: "createdOn",
    keys: [boxesOrItems],
    width,
    height,
  };

  return (
    <Card>
      <VisHeader
        maxWidthPx={width}
        heading={heading}
        visId={visId}
        onExport={onExport}
        defaultHeight={500}
        defaultWidth={1000}
        chartProps={chartProps}
      />
      <CardBody>
        <BarChart {...chartProps} />
      </CardBody>
    </Card>
  );
}
