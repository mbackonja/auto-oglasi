app.config(($routeProvider, $locationProvider) => {
  $routeProvider
    .when('/', {
      templateUrl: 'client/static/partials/main/main.component.html'
    })
    .when('/test', {
      templateUrl: 'client/static/partials/test/test.component.html'
    })
    .when('/register', {
      templateUrl: 'client/static/partials/auth/register.component.html'
    })

  $locationProvider.html5Mode(true)
})
