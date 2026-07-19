package eu.kanade.tachiyomi.extension.all.dummyextension

import eu.kanade.tachiyomi.source.model.FilterList
import eu.kanade.tachiyomi.source.model.MangasPage
import eu.kanade.tachiyomi.source.online.HttpSource

@Suppress("unused")
class DummyExtension : HttpSource() {
    override val baseUrl: String = "https://example.com"
    override val lang: String = "all"
    override val name: String = "Dummy Extension"
    override val supportsLatest: Boolean = false

    override suspend fun getPopularManga(page: Int): MangasPage =
        throw UnsupportedOperationException("This is a non-functioning Dummy Extension")

    override suspend fun getSearchManga(
        page: Int,
        query: String,
        filters: FilterList
    ): MangasPage = throw UnsupportedOperationException("This is a non-functioning Dummy Extension")
}