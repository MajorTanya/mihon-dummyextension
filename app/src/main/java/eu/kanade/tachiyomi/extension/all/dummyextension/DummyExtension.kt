package eu.kanade.tachiyomi.extension.all.dummyextension

import eu.kanade.tachiyomi.source.model.FilterList
import eu.kanade.tachiyomi.source.model.MangasPage
import eu.kanade.tachiyomi.source.model.Page
import eu.kanade.tachiyomi.source.model.SChapter
import eu.kanade.tachiyomi.source.model.SManga
import eu.kanade.tachiyomi.source.online.HttpSource

@Suppress("unused")
class DummyExtension : HttpSource() {
    override val baseUrl: String = "https://example.com"
    override val lang: String = "all"
    override val name: String = "Dummy Extension"
    override val supportsLatest: Boolean = false

    override fun chapterListParse(response: okhttp3.Response): List<SChapter> =
        throw UnsupportedOperationException("This is a non-functioning Dummy Extension")

    override fun imageUrlParse(response: okhttp3.Response): String =
        throw UnsupportedOperationException("This is a non-functioning Dummy Extension")

    override fun latestUpdatesParse(response: okhttp3.Response): MangasPage =
        throw UnsupportedOperationException("This is a non-functioning Dummy Extension")

    override fun latestUpdatesRequest(page: Int): okhttp3.Request =
        throw UnsupportedOperationException("This is a non-functioning Dummy Extension")

    override fun mangaDetailsParse(response: okhttp3.Response): SManga =
        throw UnsupportedOperationException("This is a non-functioning Dummy Extension")

    override fun pageListParse(response: okhttp3.Response): List<Page> =
        throw UnsupportedOperationException("This is a non-functioning Dummy Extension")

    override fun popularMangaParse(response: okhttp3.Response): MangasPage =
        throw UnsupportedOperationException("This is a non-functioning Dummy Extension")

    override fun popularMangaRequest(page: Int): okhttp3.Request =
        throw UnsupportedOperationException("This is a non-functioning Dummy Extension")

    override fun searchMangaParse(response: okhttp3.Response): MangasPage =
        throw UnsupportedOperationException("This is a non-functioning Dummy Extension")

    override fun searchMangaRequest(
        page: Int, query: String, filters: FilterList
    ): okhttp3.Request =
        throw UnsupportedOperationException("This is a non-functioning Dummy Extension")
}