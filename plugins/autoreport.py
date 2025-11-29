from Zohun.helpers import CMD, Emoji

__MODULE__ = "Autoreport"
__HELP__ = """
<blockquote><b>📌 Fitur Auto Report Channel, Telegram, dan Grup Privat</b>

- Kirim laporan otomatis ke **Channel, Grup Privat, dan @NoToScam Telegram**.
- Contoh: <code>.autoreport target_username atau https://t.me/channel_link</code>

<b>📌 Perintah:</b>
- <code>{0}report target_username</code> → Report user/akun.
- <code>{0}report https://t.me/channel_link</code> → Report channel atau grup</b></blockquote>.
"""

@CMD.UBOT("report")
async def _(client, message):
    msg = await message.reply("🔍 Memproses laporan otomatis...")
    
    try:
        args = message.text.split(" ", 1)
        if len(args) < 2:
            return await msg.edit("❌ Masukkan username atau link channel/grup!\nContoh: <code>.report target_username</code>")

        target = args[1]

        # 🔹 Kirim laporan ke Grup Privat
        private_group = "https://t.me/+PrivateGroupLink"  # Ganti dengan link grup privat
        report_text = f"""
🚨 <b>⚠️ LAPORAN OTOMATIS ⚠️</b> 🚨
🔹 Target: {target}
🔹 Alasan: Spam, Penipuan, atau Konten Berbahaya
🔹 Dilaporkan oleh: {message.from_user.mention}

⚠️ Silakan cek dan tindak lanjut jika diperlukan.
        """
        await client.send_message(private_group, report_text)

        # 🔹 Kirim laporan ke Channel (jika ada)
        report_channel = "@YourReportChannel"  # Ganti dengan channel report
        await client.send_message(report_channel, report_text)

        # 🔹 Kirim laporan ke Telegram @NoToScam (Official Scam Report)
        await client.send_message("@NoToScam", f"/report {target} Penipuan, Spam, atau Konten Berbahaya.")

        await msg.edit(f"✅ Laporan berhasil dikirim ke:\n- **Grup Privat**\n- **Channel Report**\n- **@NoToScam Telegram**")

    except Exception as e:
        await msg.edit(f"❌ Gagal mengirim laporan:\n<code>{str(e)}</code>")