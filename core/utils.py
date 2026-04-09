import uuid


def generate_meeting_link():
    
    meeting_id = uuid.uuid4().hex[:8]

    meeting_link = f"https://meet.jit.si/EduConnect-{meeting_id}"

    return meeting_link