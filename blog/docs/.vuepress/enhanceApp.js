export default ({
    Vue, // VuePress 正在使用的 Vue 构造函数
    options, // 附加到根实例的一些选项
    router, // 当前应用的路由实例
    siteData, // 站点元数据
    isServer, // 当前应用配置是处于 服务端渲染 或 客户端
}) => {
    siteData.pages.sort((a, b) => {
        let da = new Date(a.frontmatter.date);
        let db = new Date(b.frontmatter.date);
        return db.getTime() - da.getTime();
    });
    
    // 类别收集
    // 杂谈区域应该没有类别才对
    let categories = [];

    for (let i = 0; i < siteData.pages.length; i++) {
        let category = siteData.pages[i].frontmatter.category;
        if (category != undefined) {
            if (!categories.includes(category)) {
                categories.push(category);
            }
        }
    }

    siteData.themeConfig["categories"] = categories;
};
