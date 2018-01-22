app.directive('ad', () => {
  return {
    templateUrl: 'static/components/client/ad/ad.component.html',
    restrict: 'E',
    scope: {
      mark: '@'
    }
  }
})
