app.controller('NavbarController', ['$scope', '$location', ($scope, $location) => {
  $scope.isActive = function (viewLocation) {
    return viewLocation === $location.path()
  }
}])
