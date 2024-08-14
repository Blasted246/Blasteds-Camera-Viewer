import cv2
import tkinter as tk
from tkinter import simpledialog
import win32com.client

def list_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

def get_camera_names():
    camera_names = []
    dev_enum = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    dev_service = dev_enum.ConnectServer(".", "root\\cimv2")
    cameras = dev_service.ExecQuery("SELECT * FROM Win32_PnPEntity WHERE Description LIKE '%camera%'")
    for camera in cameras:
        camera_names.append(camera.Description)
    return camera_names

def select_camera():
    cameras = list_cameras()
    camera_names = get_camera_names()
    if not cameras:
        print("No cameras found.")
        return None
    
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    camera_str = "\n".join([f"{i}: {camera_names[i] if i < len(camera_names) else 'Camera ' + str(cam)}" for i, cam in enumerate(cameras)])
    cam_index = simpledialog.askinteger("Select Camera", f"Available cameras:\n{camera_str}\n\nEnter camera index:")
    
    root.destroy()
    return cameras[cam_index] if cam_index is not None and cam_index in range(len(cameras)) else None

def main():
    cam_index = select_camera()
    if cam_index is None:
        return
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    # Set the desired resolution to 1080p
    width = 1920
    height = 1080
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Camera Output', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()