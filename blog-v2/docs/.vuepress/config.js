
const { path } = require('@vuepress/utils')

module.exports = {
    debug: true,
    lang: 'zh-CN',
    title: 'korilin',
    description: 'korilin - 林洁彬的个人博客',
    base: "/blog/",
    head: [
        ["link", { rel: "icon", href: "/korilin.png" }],
        ["script", { src: "/statistics.js" }],
    ],
    theme: path.resolve(__dirname, 'G:/main/blog-v2/docs/.vuepress/theme'),
    themeConfig: {
      logo: '/korilin.png',
      navbar: [
          { text: "主页", link: "/" },
          { text: "技术长文", link: "/archive/" },
          { text: "笔记杂谈", link: "/tittle-tattle/" },
          { text: "深圳KUG", link: "https://korilin.com/KUGshenzhen/" },
      ],
      smoothScroll: true,
      socialPlatform: [
          {
              name: "github",
              href: "https://github.com/korilin",
              icon: "/icon/github.png",
          },
          {
              name: "twitter",
              href: "https://twitter.com/korilin_dev",
              icon: "/icon/twitter.png",
          },
          {
              name: "telegram",
              href: "https://t.me/korilin",
              icon: "/icon/telegram.png",
          },
      ],
    },
  }