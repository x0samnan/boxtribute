import {
  Box,
  Heading,
  LinkBox,
  LinkOverlay,
  List,
  ListItem,
  Text,
} from "@chakra-ui/react";
import { isToday } from "date-fns";
import isFuture from "date-fns/isFuture";
import isPast from "date-fns/isPast";
import _ from "lodash";
import { ReactElement } from "react";
import { useParams } from "react-router-dom";
import {
  DistributionEventDetails,
  DistributionEventState,
} from "views/Distributions/types";

const ListOfEvents = ({
  distributionEventsListData,
  heading,
}: {
  distributionEventsListData: DistributionEventDetails[];
  heading?: ReactElement;
}) => {
  const { getDistroEventDetailUrlById } = useGetUrlForResourceHelpers();

  return (
    <>
      {heading != null && heading}
      <List>
        {distributionEventsListData.map((distributionEventData) => (
          <ListItem key={distributionEventData.id} my={10}>
            <LinkBox maxW="sm" p="5" borderWidth="1px" rounded="md">
              <Box
                as="time"
                dateTime={distributionEventData.plannedStartDateTime.toUTCString()}
              >
                {distributionEventData.plannedStartDateTime.toDateString()} (
                {distributionEventData.plannedStartDateTime.toLocaleTimeString()}{" "}
                -{" "}
                {distributionEventData.plannedEndDateTime.toLocaleTimeString()})
              </Box>
              <Heading size="md" my="2">
                <LinkOverlay
                  href={getDistroEventDetailUrlById(distributionEventData.id)}
                >
                  {distributionEventData.distributionSpot.name}{" "}
                  {!!distributionEventData.name && (
                    <>({distributionEventData.name})</>
                  )}
                </LinkOverlay>
              </Heading>

              <Text>
                <b>State: </b>
                {distributionEventData.state}
              </Text>
            </LinkBox>
          </ListItem>
        ))}
      </List>
    </>
  );
};

// TODO: move this out into own file
// and reuse it in other views as well
const useGetUrlForResourceHelpers = () => {
  const baseId = useParams<{ baseId: string }>().baseId;
  const getDistroSpotDetailUrlById = (distroSpotId: string) =>
    `/bases/${baseId}/distributions/spots/${distroSpotId}`;

  const getDistroEventDetailUrlById = (distroEventId: string) =>
    `/bases/${baseId}/distributions/events/${distroEventId}`;

  return {
    getDistroSpotDetailUrlById,
    getDistroEventDetailUrlById,
  };
};

const UpcomingDistributions = ({
  distributionEventsData,
}: {
  distributionEventsData: DistributionEventDetails[];
}) => {
  const sortedDistroEvents = _.chain(distributionEventsData)
    .orderBy((el) => el.plannedStartDateTime, "desc")
    .value();
  // .groupBy(el => el.state)

  const todaysAndUpcomingDistroEvents = sortedDistroEvents.filter((el) =>
    isFuture(el.plannedStartDateTime) || isToday(el.plannedEndDateTime)
  );
  const upcomingDistroEventsToday = todaysAndUpcomingDistroEvents.filter((el) =>
    isToday(el.plannedStartDateTime)
  );
  const upcomingDistroEventsAfterToday = todaysAndUpcomingDistroEvents.filter((el) =>
  !isToday(el.plannedStartDateTime)
  );

  const pastDistroEvents = sortedDistroEvents.filter((el) =>
    isPast(el.plannedStartDateTime)
  );
  const pastNonCompletedDistroEvents = pastDistroEvents.filter(
    (el) => el.state !== DistributionEventState.Completed
  );
  const pastCompletedDistroEvents = sortedDistroEvents.filter(
    (el) => el.state === DistributionEventState.Completed
  );

  const hasUpcomingDistroEvents = todaysAndUpcomingDistroEvents.length > 0;
  const hasUpcomingDistroEventsToday = upcomingDistroEventsToday.length > 0;
  const hasUpcomingDistroEventsAfterToday =
    upcomingDistroEventsAfterToday.length > 0;
  const showHeadingForUpcomingDistroEventsAfterTodaySection =
    hasUpcomingDistroEventsToday;

  const hasPastDistroEvents = pastDistroEvents.length > 0;
  const hasPastCompletedDistroEvents = pastCompletedDistroEvents.length > 0;
  const hasPastNonCompletedDistroEvents =
    pastNonCompletedDistroEvents.length > 0;

  return (
    <List>
      {hasUpcomingDistroEvents && (
        <ListItem>
          <Heading as="h4">Upcoming</Heading>
          <List>
            {hasUpcomingDistroEventsToday && (
              <ListItem>
                <ListOfEvents
                  distributionEventsListData={upcomingDistroEventsToday}
                  heading={
                    <Heading as="h5" size={"md"}>
                      Today
                    </Heading>
                  }
                />
              </ListItem>
            )}
            {hasUpcomingDistroEventsAfterToday && (
              <ListItem>
                <ListOfEvents
                  distributionEventsListData={upcomingDistroEventsAfterToday}
                  heading={
                    showHeadingForUpcomingDistroEventsAfterTodaySection ? (
                      <Heading as="h5" size={"md"}>
                        Later
                      </Heading>
                    ) : undefined
                  }
                />
              </ListItem>
            )}
          </List>
        </ListItem>
      )}

      {hasPastDistroEvents && (
        <ListItem>
          <Heading as="h4">Past</Heading>
          <List>
            {hasPastNonCompletedDistroEvents && (
              <ListItem>
                <ListOfEvents
                  distributionEventsListData={pastNonCompletedDistroEvents}
                  heading={
                    <Heading as="h5" size={"md"}>
                      Not yet completed
                    </Heading>
                  }
                />
              </ListItem>
            )}
            {hasPastCompletedDistroEvents && (
              <ListItem>
                <ListOfEvents
                  distributionEventsListData={pastCompletedDistroEvents}
                  heading={
                    <Heading as="h5" size={"md"}>
                      Completed
                    </Heading>
                  }
                />
              </ListItem>
            )}
          </List>
        </ListItem>
      )}
    </List>
  );
};

export default UpcomingDistributions;
