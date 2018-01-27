let app = angular.module('app', ['ngRoute'], ($interpolateProvider) => {
  $interpolateProvider.startSymbol('[[')
  $interpolateProvider.endSymbol(']]')
})

app.controller('NavbarController', ['$scope', '$location', ($scope, $location) => {
  $scope.isActive = function (viewLocation) {
    return viewLocation === $location.path()
  }
}])
