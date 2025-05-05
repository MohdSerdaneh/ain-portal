def student_directory_path(inst, file_name):
    """
    Returns the upload path for a student's avatar image.

    Example path:
    student_profile_images/username/filename.png
    """
    return f"student_profile_images/{inst.user}/{file_name}"


def teacher_directory_path(inst, file_name):
    """
    Returns the upload path for a teacher's avatar image.

    Example path:
    teacher_profile_images/username/filename.png
    """
    return f"teacher_profile_images/{inst.user}/{file_name}"
