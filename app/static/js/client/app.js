let app = angular.module('clientApp', ['ngRoute'], ($interpolateProvider) => {
  $interpolateProvider.startSymbol('[[')
  $interpolateProvider.endSymbol(']]')
})

app.config(($routeProvider, $locationProvider) => {
  $routeProvider
    .when('/', {
      templateUrl: 'static/components/client/main/main.component.html'
    })
    .when('/test', {
      templateUrl: 'static/components/client/test/test.component.html'
    })

  $locationProvider.html5Mode(true)
})
