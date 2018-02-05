app.config(($routeProvider, $locationProvider) => {
  $routeProvider
    .when('/admin-panel', {
      templateUrl: 'admin/static/partials/admin-panel.component.html',
      resolve: {
        auth: (ActiveUserService) => {
          return ActiveUserService.hasAccess('admin')
        }
      }
    })
})
