
let config = require('./webpack.config')

// Configure webpack-dev-server
config.devServer = {
  inline: true,
  stats: { colors: true },
  contentBase: "./src/public/",

  proxy: {
    '/api': {
        target: 'http://localhost:5000',
        secure: false
    }
  }


};

module.exports = config;
