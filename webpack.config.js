const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  entry: './frontend/src/index.js',
  output: {
    path: path.resolve('./static/webpack_bundles/'),
    filename: "[name]-[fullhash].js",
    publicPath: '/static/webpack_bundles/'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        },
      },
    ],
  },
  plugins: [
    new BundleTracker({
      path: __dirname,
      filename: 'webpack-stats.json'
    }),
  ],
};