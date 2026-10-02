from hashlib import sha256
from io import BytesIO

import streamlit as st
from PIL import Image
from PIL import UnidentifiedImageError


def _append_photo(photo_bytes):
    image_hash = sha256(photo_bytes).hexdigest()
    if image_hash in st.session_state.attendance_image_hashes:
        return False

    try:
        with Image.open(BytesIO(photo_bytes)) as image:
            photo = image.convert('RGB')
    except (OSError, UnidentifiedImageError):
        st.warning('Could not read an uploaded image.')
        return False

    st.session_state.attendance_images.append(photo)
    st.session_state.attendance_image_hashes.add(image_hash)
    return True


@st.dialog("Capture or upload photos")
def add_photos_dialog():

    st.write('Add classroom photos to scan for attendance')

    if 'attendance_image_hashes' not in st.session_state:
        st.session_state.attendance_image_hashes = set()

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('Camera', type=type_camera, width='stretch'):
            st.session_state.photo_tab = 'camera'



    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('Upload photos', type=type_upload, width='stretch'):
            st.session_state.photo_tab = 'upload'

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
        if cam_photo and _append_photo(cam_photo.getvalue()):
            st.toast('Photo Captured')
            st.rerun()


    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader( 'choose image files', type=['jpg', 'png', 'jpeg' ], accept_multiple_files=True, key='dialog_upload')

        if uploaded_files:
            added_photos = False
            for f in uploaded_files:
                added_photos = _append_photo(f.getvalue()) or added_photos

            if added_photos:
                st.toast('Photo Uploaded Successfully')
                st.rerun()

    st.divider()
    if st.button('Done', type='primary', width='stretch'):
        st.rerun()