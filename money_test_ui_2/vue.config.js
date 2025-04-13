const { defineConfig } = require('@vue/cli-service')
// vue.config.js
module.exports= defineConfig({
  devServer: {
    proxy: {
      '/api':{
        target: 'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/api':''
        }
      }
    }
  }
})

