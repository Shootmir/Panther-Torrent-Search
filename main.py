# (c) @AbirHasan2005 & Jigar Varma & Hemanta Pokharel & Akib Hridoy

import asyncio
from pyrogram import Client, filters
from pyrogram.errors import QueryIdInvalid, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent

from configs import Config
from tool import SearchYTS, SearchAnime, Search1337x, SearchPirateBay

TorrentBot = Client(session_name=Config.SESSION_NAME, api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)
DEFAULT_SEARCH_MARKUP = [
                    [InlineKeyboardButton("𝗦𝗲𝗮𝗿𝗰𝗵 𝗬𝗧𝗦 𝗠𝗼𝘃𝗶𝗲𝘀 📺🔥", switch_inline_query_current_chat="!yts "),
                     InlineKeyboardButton("𝗦𝗲𝗮𝗿𝗰𝗵 𝗜𝗻 1337x 🔥", switch_inline_query_current_chat="")],
                    [InlineKeyboardButton("𝗦𝗲𝗮𝗿𝗰𝗵 𝗔𝗻𝘆 𝗧𝗼𝗿𝗿𝗲𝗻𝘁 𝗶𝗻 𝗣𝗶𝗿𝗮𝘁𝗲𝗯𝗮𝘆 ☠️🍁", switch_inline_query_current_chat="!pb ")],
                    [InlineKeyboardButton("𝗝𝗼𝗶𝗻 𝗚𝗿𝗼𝘂𝗽 🌷 ", url="https://t.me/joinchat/bZfGkMGaGwswZjI1"),
                     InlineKeyboardButton("𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗠𝗲 🥰🌷", url="https://t.me/Ravindu_Deshanz")]
                ]


@TorrentBot.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    try:
        await message.reply_sticker("CAACAgUAAxkBAAEC11VhMKoiYfFiHo9BxHHaD2M2rMIW0gACDgUAArD8gFX57AkpeFVIYiAE")
        await message.reply_text(
            text="𝗛𝗶 {{message.from_user.first_name} ✨💐...𝗜 𝗮𝗺 𝗮 𝗣𝗼𝘄𝗲𝗿𝗳𝘂𝗹 𝗧𝗼𝗿𝗿𝗲𝗻𝘁 𝗦𝗲𝗮𝗿𝗰𝗵 𝗕𝗼𝘁 𝗶𝗻 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 🥰🔥\n\n"
                 "𝗠𝗮𝗱𝗲 𝗳𝗼𝗿 𝗣𝗮𝗻𝘁𝗵𝗲𝗿 𝗠𝗶𝗿𝗿𝗼𝗿 𝗚𝗿𝗼𝘂𝗽🥰✨\n\n"
                 "𝗬𝗧𝗦 , 𝗣𝗶𝗿𝗮𝘁𝗲𝗕𝗮𝘆 𝗮𝗻𝗱 13377𝘅 𝗔𝗿𝗲 𝗦𝘂𝗽𝗽𝗿𝘁𝗲𝗱 🔥\n\n"
                 "𝗟𝗶𝘃𝗲 𝗼𝗻 𝗛𝗲𝗿𝗼𝗸𝘂 𝗦𝗲𝗿𝘃𝗲𝗿 🔥\n\n"
                 "𝗣𝗿𝗼𝗷𝗲𝗰𝘁 𝗯𝘆 @Ravindu_Deshanz ⚡️\n\n"
                 "/help 𝗙𝗼𝗿 𝗠𝗼𝗿𝗲 𝗢𝗽𝘁𝗶𝗼𝗻𝘀 🙃❤️",
            disable_web_page_preview=True,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(DEFAULT_SEARCH_MARKUP)
        )
    except FloodWait as e:
        print(f"[{Config.SESSION_NAME}] - Sleeping for {e.x}s")
        await asyncio.sleep(e.x)
        await start_handler(_, message)


@TorrentBot.on_inline_query()
async def inline_handlers(_, inline: InlineQuery):
    search_ts = inline.query
    answers = []
    if search_ts == "":
        answers.append(
            InlineQueryResultArticle(
                title="Search Something ...",
                description="Search For Torrents ...",
                input_message_content=InputTextMessageContent(
                    message_text="Search for Torrents from Inline!",
                    parse_mode="Markdown"
                ),
                reply_markup=InlineKeyboardMarkup(DEFAULT_SEARCH_MARKUP)
            )
        )
    elif search_ts.startswith("!pb"):
        query = search_ts.split(" ", 1)[-1]
        if (query == "") or (query == " "):
            answers.append(
                InlineQueryResultArticle(
                    title="!pb [text]",
                    description="Search For Torrent in ThePirateBay ...",
                    input_message_content=InputTextMessageContent(
                        message_text="`!pb [text]`\n\nSearch ThePirateBay Torrents from Inline!",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔍Search Again", switch_inline_query_current_chat="!pb ")]])
                )
            )
        else:
            torrentList = await SearchPirateBay(query)
            if not torrentList:
                answers.append(
                    InlineQueryResultArticle(
                        title="No Torrents Found in ThePirateBay!",
                        description=f"Can't find torrents for {query} in ThePirateBay !!",
                        input_message_content=InputTextMessageContent(
                            message_text=f"No Torrents Found For `{query}` in ThePirateBay !!",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!pb ")]])
                    )
                )
            else:
                for i in range(len(torrentList)):
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"Seeders: {torrentList[i]['Seeders']}, Leechers: {torrentList[i]['Leechers']}\nSize: {torrentList[i]['Size']}",
                            input_message_content=InputTextMessageContent(
                                message_text=f"**🗂Category:** `{torrentList[i]['Category']}`\n"
                                             f"**📝Name:** `{torrentList[i]['Seeders']}`\n"
                                             f"**📊Size:** `{torrentList[i]['Size']}`\n"
                                             f"**📦Seeders:** `{torrentList[i]['Seeders']}`\n"
                                             f"**🔗Leechers:** `{torrentList[i]['Leechers']}`\n"
                                             f"**📤Uploader:** `{torrentList[i]['Uploader']}`\n"
                                             f"**📭Uploaded :** {torrentList[i]['Date']}**\n\n"
                                             f"**🗒Magnet:**\n`{torrentList[i]['Magnet']}`\n\n ✅ Powered By @SDBOTs_inifinity  ",
                                parse_mode="Markdown"
                            ),
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("🔍Search Again", switch_inline_query_current_chat="!pb ")]])
                        )
                    )
    elif search_ts.startswith("!yts"):
        query = search_ts.split(" ", 1)[-1]
        if (query == "") or (query == " "):
            answers.append(
                InlineQueryResultArticle(
                    title="!yts [text]",
                    description="Search For Torrent in YTS ...",
                    input_message_content=InputTextMessageContent(
                        message_text="`!yts [text]`\n\nSearch YTS Torrents from Inline!",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("🔍Search Again", switch_inline_query_current_chat="!yts ")]])
                )
            )
        else:
            torrentList = await SearchYTS(query)
            if not torrentList:
                answers.append(
                    InlineQueryResultArticle(
                        title="No Torrents Found!",
                        description=f"Can't find YTS torrents for {query} !!",
                        input_message_content=InputTextMessageContent(
                            message_text=f"No YTS Torrents Found For `{query}`",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!yts ")]])
                    )
                )
            else:
                for i in range(len(torrentList)):
                    dl_links = "- " + "\n\n- ".join(torrentList[i]['Downloads'])
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"Language: {torrentList[i]['Language']}\nLikes: {torrentList[i]['Likes']}, Rating: {torrentList[i]['Rating']}",
                            input_message_content=InputTextMessageContent(
                                message_text=f"**🔐Genre:** `{torrentList[i]['Genre']}`\n"
                                             f"**🏷Name:** `{torrentList[i]['Name']}`\n"
                                             f"**📝Language:** `{torrentList[i]['Language']}`\n"
                                             f"**🖇Likes:** `{torrentList[i]['Likes']}`\n"
                                             f"**🌟Rating:** `{torrentList[i]['Rating']}`\n"
                                             f"**📊Duration:** `{torrentList[i]['Runtime']}`\n"
                                             f"**🗓Released on {torrentList[i]['ReleaseDate']}**\n\n"
                                             f"**🔗Torrent Download Links:**\n{dl_links}\n\n ✅ Powered By @SDBOTs_inifinity",
                                parse_mode="Markdown",
                                disable_web_page_preview=True
                            ),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔍Search Again", switch_inline_query_current_chat="!yts ")]]),
                            thumb_url=torrentList[i]["Poster"]
                        )
                    )
    elif search_ts.startswith("!a"):
        query = search_ts.split(" ", 1)[-1]
        if (query == "") or (query == " "):
            answers.append(
                InlineQueryResultArticle(
                    title="!a [text]",
                    description="Search For Torrents for Anime ...",
                    input_message_content=InputTextMessageContent(
                        message_text="`!a [text]`\n\nSearch Anime Torrents from Inline!",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("🔍Search Again", switch_inline_query_current_chat="!a ")]])
                )
            )
        else:
            torrentList = await SearchAnime(query)
            if not torrentList:
                answers.append(
                    InlineQueryResultArticle(
                        title="No Anime Torrents Found!",
                        description=f"Can't find Anime torrents for {query} !!",
                        input_message_content=InputTextMessageContent(
                            message_text=f"No Anime Torrents Found For `{query}`",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!a ")]])
                    )
                )
            else:
                for i in range(len(torrentList)):
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"Seeders: {torrentList[i]['Seeder']}, Leechers: {torrentList[i]['Leecher']}\nSize: {torrentList[i]['Size']}",
                            input_message_content=InputTextMessageContent(
                                message_text=f"**🗂Category:** `{torrentList[i]['Category']}`\n"
                                             f"**📝Name:** `{torrentList[i]['Name']}`\n"
                                             f"**📦Seeders:** `{torrentList[i]['Seeder']}`\n"
                                             f"**🔗Leechers:** `{torrentList[i]['Leecher']}`\n"
                                             f"**📊Size:** `{torrentList[i]['Size']}`\n"
                                             f"**📭Uploaded on:** `{torrentList[i]['Date']}`\n\n"
                                             f"**🗒Magnet:** \n`{torrentList[i]['Magnet']}`\n\n✅ Powered By @SDBOTs_inifinity",
                                parse_mode="Markdown"
                            ),
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("🔍Search Again", switch_inline_query_current_chat="!a ")]]
                            )
                        )
                    )
    else:
        torrentList = await Search1337x(search_ts)
        if not torrentList:
            answers.append(
                InlineQueryResultArticle(
                    title="No Torrents Found!",
                    description=f"Can't find torrents for {search_ts} !!",
                    input_message_content=InputTextMessageContent(
                        message_text=f"No Torrents Found For `{search_ts}`",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="")]])
                )
            )
        else:
            for i in range(len(torrentList)):
                answers.append(
                    InlineQueryResultArticle(
                        title=f"{torrentList[i]['Name']}",
                        description=f"Seeders: {torrentList[i]['Seeders']}, Leechers: {torrentList[i]['Leechers']}\nSize: {torrentList[i]['Size']}, Downloads: {torrentList[i]['Downloads']}",
                        input_message_content=InputTextMessageContent(
                            message_text=f"**Category:** `{torrentList[i]['Category']}`\n"
                                         f"**Name:** `{torrentList[i]['Name']}`\n"
                                         f"**Language:** `{torrentList[i]['Language']}`\n"
                                         f"**Seeders:** `{torrentList[i]['Seeders']}`\n"
                                         f"**Leechers:** `{torrentList[i]['Leechers']}`\n"
                                         f"**Size:** `{torrentList[i]['Size']}`\n"
                                         f"**Downloads:** `{torrentList[i]['Downloads']}`\n"
                                         f"__Uploaded by {torrentList[i]['UploadedBy']}__\n"
                                         f"__Uploaded {torrentList[i]['DateUploaded']}__\n"
                                         f"__Last Checked {torrentList[i]['LastChecked']}__\n\n"
                                         f"**Magnet:**\n`{torrentList[i]['Magnet']}`\n\n✅ Powered By @SDBOTs_inifinity",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("🔍Search Again", switch_inline_query_current_chat="")]]
                        ),
                        thumb_url=torrentList[i]['Poster']
                    )
                )
    try:
        await inline.answer(
            results=answers,
            cache_time=0
        )
        print(f"[{Config.SESSION_NAME}] - Answered Successfully - {inline.from_user.first_name}")
    except QueryIdInvalid:
        print(f"[{Config.SESSION_NAME}] - Failed to Answer - {inline.from_user.first_name} - Sleeping for 5s")
        await asyncio.sleep(5)
        try:
            await inline.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Error: Search timed out!",
                switch_pm_parameter="start",
            )
        except QueryIdInvalid:
            print(f"[{Config.SESSION_NAME}] - Failed to Answer Error - {inline.from_user.first_name} - Sleeping for 5s")
            await asyncio.sleep(5)


TorrentBot.run()
