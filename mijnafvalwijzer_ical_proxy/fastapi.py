from fastapi.responses import Response


class CalendarResponse(Response):
    media_type = "text/calendar"
