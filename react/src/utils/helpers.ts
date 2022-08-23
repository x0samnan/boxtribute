export const getISODateTimeFromDateAndTimeString = (date: Date, timeString: string) => {
  const [hours, minutes] = timeString.split(':').map(Number);
  const dateTime = new Date(date);
  dateTime.setHours(hours);
  dateTime.setMinutes(minutes);
  return dateTime;
}

export const weekDayNumberToWeekDayName = (weekDayNumber: number) => {
  const weekDayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  return weekDayNames[weekDayNumber];
}

export const getDateNormalizedDateTime = (dateTime: Date) => {
  const newDate = new Date(dateTime);
  newDate.setHours(0,0,0,0);
  return newDate;
}
