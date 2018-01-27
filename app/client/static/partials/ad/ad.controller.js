app.directive('ad', () => {
  return {
    templateUrl: 'client/static/partials/ad/ad.component.html',
    restrict: 'E',
    scope: {
      product: '='
    }
  }
})
