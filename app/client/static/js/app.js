app.config(($routeProvider, $locationProvider) => {
  $routeProvider
    .when('/', {
      templateUrl: 'client/static/partials/main/main.component.html'
    })
    .when('/test', {
      templateUrl: 'client/static/partials/test/test.component.html'
    })
    .when('/register', {
      templateUrl: 'client/static/partials/auth/register.component.html',
      resolve: {
        'auth': (ActiveUserService) => {
          return ActiveUserService.hasAccess('guest')
        }
      }
    })
    .when('/login', {
      templateUrl: 'client/static/partials/auth/login.component.html',
      resolve: {
        'auth': (ActiveUserService) => {
          return ActiveUserService.hasAccess('guest')
        }
      }
    })

  $locationProvider.html5Mode(true)
})
  .run(($rootScope, $location) => {
    $rootScope.$on('$routeChangeError', function (event, current, previous, rejection) {
      if (rejection === 'Not guest' || rejection === 'Not logged' || rejection === 'Not administrator') {
        $location.path('/')
      }
    })
  })
