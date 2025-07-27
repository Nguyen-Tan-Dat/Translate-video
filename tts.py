import os
import uuid
import asyncio
import edge_tts


def text_to_speech(text, output_dir, rate="+0%"):
    output_path = os.path.join(output_dir, f"{uuid.uuid4()}.mp3")

    async def run():
        communicate = edge_tts.Communicate(text=text, voice="vi-VN-HoaiMyNeural", rate=rate)
        await communicate.save(output_path)

    asyncio.run(run())
    return output_path
