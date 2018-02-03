app.config(($routeProvider, $locationProvider) => {
  $routeProvider
    .when('/', {
      templateUrl: 'client/static/partials/main/main.component.html'
    })
    .when('/register', {
      templateUrl: 'client/static/partials/auth/register.component.html',
      resolve: {
        auth: (ActiveUserService) => {
          return ActiveUserService.hasAccess('guest')
        }
      }
    })
    .when('/login', {
      templateUrl: 'client/static/partials/auth/login.component.html',
      resolve: {
        auth: (ActiveUserService) => {
          return ActiveUserService.hasAccess('guest')
        }
      }
    })
    .when('/my-profile', {
      templateUrl: 'client/static/partials/my-profile/my-profile.component.html',
      resolve: {
        auth: (ActiveUserService) => {
          return ActiveUserService.hasAccess('member')
        }
      }
    })
    .when('/view-car/:id', {
      templateUrl: 'client/static/partials/car/car.component.html'
    })
    .when('/my-cars', {
      templateUrl: 'client/static/partials/my-cars/my-cars.component.html',
      resolve: {
        auth: (ActiveUserService) => {
          return ActiveUserService.hasAccess('member')
        }
      }
    })
    .when('/car/:action/:id?', {
      templateUrl: 'client/static/partials/add-edit-car/add-edit-car.component.html',
      resolve: {
        auth: (ActiveUserService) => {
          return ActiveUserService.hasAccess('member')
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
