# devicedata.py

import xml.etree.ElementTree as ET
from datetime import datetime
from connection import get_db_connection

def parse_and_insert_data(xml_data):
    """
    Parses XML data and inserts it into the database.
    """
    try:
        # Parse the XML data
        print("XML DATA RECIEVED\n", xml_data)
        xml_data = xml_data.replace(b'\x00', b'')
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
        return """<?xml version="1.0"?><Message><Request>UploadError</Request><Error>Invalid XML</Error></Message>"""

    try:
        # Extract fields
        device_uid = root.find('DeviceUID').text
        terminal_id = root.find('TerminalID').text
        device_serial_no = root.find('DeviceSerialNo').text
        trans_id = root.find('TransID').text
        event = root.find('Event').text
        year = root.find('Year').text
        month = root.find('Month').text
        day = root.find('Day').text
        hour = root.find('Hour').text
        minute = root.find('Minute').text
        second = root.find('Second').text
        user_id = root.find('UserID').text
        attend_stat = root.find('AttendStat').text
        verif_mode = root.find('VerifMode').text

        # Create datetime object
        timestamp = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

        # Log the received data (optional, for debugging)
        print(f"Received data - Device UID: {device_uid}, Terminal ID: {terminal_id}, Device Serial No: {device_serial_no}, "
              f"TransID: {trans_id}, Event: {event}, Timestamp: {timestamp}, UserID: {user_id}, "
              f"AttendStat: {attend_stat}, VerifMode: {verif_mode}")

        # Insert data into the raw table
        conn = get_db_connection()
        cur = conn.cursor()

        insert_query = """
        INSERT INTO raw_attendance (device_uid, terminal_id, device_serial_no, trans_id, event, timestamp, user_id, attend_stat, verif_mode)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        cur.execute(insert_query, (
            device_uid, terminal_id, device_serial_no, trans_id, event, timestamp, user_id, attend_stat, verif_mode))

        # Commit and close connection
        conn.commit()
        cur.close()
        conn.close()

        # Return success response
        return f"""<?xml version="1.0"?><Message><Request>UploadedLog</Request><TransID>{trans_id}</TransID><Count>1</Count></Message>"""

    except Exception as e:
        print(f"Error processing data: {e}")
        return """<?xml version="1.0"?><Message><Request>UploadError</Request><Error>Data Processing Error</Error></Message>"""
