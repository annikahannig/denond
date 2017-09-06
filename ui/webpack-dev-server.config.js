
let config = require('./webpack.config')

// Configure webpack-dev-server
config.devServer = {
  inline: true,
  stats: { colors: true },
  contentBase: "./build/",

  proxy: {
    '/api': {
        target: 'http://localhost:5000',
        secure: false
    }
  }


};

module.exports = config;
