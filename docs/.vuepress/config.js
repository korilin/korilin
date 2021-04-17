module.exports = {
    title: "Kori Lin",
    description: "Kori Lin - 林洁彬的个人博客",
    base: "/blog/",
    head: [["link", { rel: "icon", href: "/hero.jpg" }]],
    themeConfig: {
        logo: "/hero.jpg",
        nav: [
            { text: "主页", link: "/" },
            { text: "文章", link: "/archive/" },
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
};
