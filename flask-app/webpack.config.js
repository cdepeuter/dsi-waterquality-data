module.exports = {
    cache: true,
    entry: './static/src/app.js',
    output: {
        filename: './static/build/main.js'
    },
    devtool: 'source-map',
    module: {
        loaders: [
        {
            test: /\.js$/,
            loader: 'babel-loader',
            query: {
                presets: ['es2015', 'react', 'stage-0']
            }
        },
        { 
            test: /\.css$/, 
            loader: "style-loader!css-loader" 
        },
        {
            test: /\.json$/,
            loader: 'json'
          },
          {
            test: /\.(jpg|png|gif|eot|svg|ttf|woff|woff2)(\?.*)?$/,
            loader: 'file',
            query: {
              name: 'static/media/[name].[hash:8].[ext]'
            }
          },
        ]
    }
};