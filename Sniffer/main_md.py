import re
from scapy.all import *
from datetime import datetime

def process_packet(packet, output_file):
    if packet.haslayer(Raw):
        try:
            raw_data = packet[Raw].load.decode('utf-8', errors='ignore')
           
            pattern = re.compile(r'<([^<>]+)>([^<>]*)</?>')
            matches = pattern.findall(raw_data)
            if matches:
                with open(output_file, 'a', encoding='utf-8') as f:
                    for tag, content in matches:
                        final_data = f'<{tag}>{content}</>'
                        letter_count = len(final_data)
                        
                        # Split the raw data by any non-printable or unreadable characters
                        parts = re.split(r'[^\w\s]', raw_data)
                        parts = [part for part in parts if part.strip()]  # Remove empty parts
                        parts.reverse()

                        name = title = chat_bubble = avatar = avatar_frame = ""

                        if len(parts) > 0:
                            name = parts[0]
                        if len(parts) > 1:
                            title = parts[1]
                        if len(parts) > 2:
                            chat_bubble = parts[2]
                        if len(parts) > 3:
                            avatar = parts[3]
                        if len(parts) > 4:
                            avatar_frame = parts[4]

                        if title.endswith("s Mentor,0"):
                            # Combine the title with the previous part
                            title = f"{parts[2]} {title}".replace(",0", "")
                            chat_bubble = ""

                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                       
                        # Write in Markdown format
                        f.write(f"## Packet Capture: {timestamp}\n\n")
                        f.write(f"- **Data**: `{final_data}`\n")
                        f.write(f"- **Letter Count**: {letter_count}\n")
                        f.write(f"- **Name**: {name}\n")
                        f.write(f"- **Title**: {title}\n")
                        f.write(f"- **Chat Bubble**: {chat_bubble}\n")
                        f.write(f"- **Avatar**: {avatar}\n")
                        f.write(f"- **Avatar Frame**: {avatar_frame}\n")
                        # f.write(f"- **Raw Data**: ```{raw_data}```\n")
                        f.write("---\n")
        except UnicodeDecodeError:
            print("UnicodeDecodeError: Cannot decode packet data.")
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    output_file = "extracted_data.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Network Packet Capture Log\n\n")
   
    def packet_callback(packet):
        process_packet(packet, output_file)

    sniff(filter="host 43.159.31.173 and port 30031", prn=packet_callback)

if __name__ == "__main__":
    main()