process.traceDeprecation = true;
const mf_config = require("@patternslib/dev/webpack/webpack.mf");
const package_json = require("./package.json");
const package_json_mockup = require("@plone/mockup/package.json");
const package_json_patternslib = require("@patternslib/patternslib/package.json");
const path = require("path");
const webpack_config = require("@patternslib/dev/webpack/webpack.config").config;

module.exports = () => {
    let config = {
        entry: {
            "relatedmedia.min": path.resolve(__dirname, "resources/index.js"),
            "relatedimages-gallery.min": path.resolve(__dirname, "resources/relatedimages-gallery.js"),
        },
    };

    config = webpack_config({
        config: config,
        package_json: package_json,
    });
    config.output.path = path.resolve(__dirname, "collective/behavior/relatedmedia/resources/bundles");

    config.plugins.push(
        mf_config({
            name: "relatedmedia",
            filename: "relatedmedia-remote.min.js",
            remote_entry: config.entry["relatedmedia.min"],
            dependencies: {
                ...package_json_patternslib.dependencies,
                ...package_json_mockup.dependencies,
                ...package_json.dependencies,
            },
        })
    );

    if (process.env.NODE_ENV === "development") {
        config.devServer.port = "8011";
        config.devServer.static.directory = path.resolve(__dirname, "./resources/");
    }

    // console.log(JSON.stringify(config, null, 4));

    return config;
};
