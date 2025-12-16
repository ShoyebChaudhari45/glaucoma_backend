from extensions import fs


def save_image_to_gridfs(file, user_email):
    file_id = fs.put(
        file.read(),
        filename=file.filename,
        content_type=file.content_type,
        user_email=user_email
    )
    return file_id


def delete_image_from_gridfs(file_id):
    fs.delete(file_id)
