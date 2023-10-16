import { extract } from '@extractus/article-extractor'

//imort news_links.json and iterate over it
const news_links = require('./bun_jsons/news_links.json')
for (const link of news_links) {
    //extract the article
    const article = await extract(link)
    //save the article
    console.log(article)
}
