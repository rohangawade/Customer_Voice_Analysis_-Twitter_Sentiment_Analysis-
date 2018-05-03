 $(document).ready(function(){$('#myModal1').foundation('reveal', 'open')});
var app = angular.module('myApp', [ 'googlechart', 'angularUtils.directives.dirPagination','ionic']);
app.controller('foreseeing',['$scope', '$http', '$timeout', 'Chart', "$window", "$location", function($scope, $http, $timeout, Chart, $window, $location) {
    
    $scope.dateformat = ["YYYY-MM", "YYYY-MM-DD", "DD-MM-YYYY","MM-YYYY","YYYYMM"];
    $scope.outlierfilter = ["Remove"];   
    $scope.singlelinechart=[];
    $scope.multi=[];
    $scope.meanandstd=[];
    $scope.decomposition=[];
    $scope.acf=[];
    $scope.pacf=[];
    $scope.ma=[];
    $scope.lag=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,40,50]
    $scope.algo=["ARIMA/AR/MA","HoltWinter Additive","HoltWinter Multiplicative","HoltWinter Linear", "EWMA"]
    $scope.slag=[0,1]
    $scope.ar=[];
    $scope.arima=[];
    $scope.outliermethods=['Remove 2 Sigmas','Remove 3 Sigmas','None'];

$scope.showLoader = function()
{     
      $http.post("/col")
      .success(function(response, status, headers, config) {
      console.log("col")     
      $scope.brand=response;
      console.log(response)
      })
    
   var data1={'date':$scope.datecol,'dateformat':$scope.dateformat12,'filtercol':$scope.filtercol,'quantity':$scope.quantitycol}


      $http.post("/uniquefilter",data1)
      .success(function(response, status, headers, config) {   
      console.log("uniquefilter") ;       
      console.log(response);
      $scope.brands=response;
      })

      
  }

  $scope.comparemodels = function() {
     if($scope.brandname != undefined){
       var br=$scope.brandname
     }
     else{
       var br= 'AM SURGICAL'
      
     }
      if($scope.p != undefined){
       var pp= $scope.p
     }
     else{
       var pp= 3
      
     }
      if($scope.d != undefined){
       var dd=$scope.d
     }
     else{
       var dd= 0
      
     }
      if($scope.q != undefined){
       var qq= $scope.q
     }
     else{
       var qq= 3
      
     }
      if($scope.spanewma != undefined){
       var sp= $scope.spanewma
     }
     else{
       var sp= 7
      
     }
     if($scope.hwlag != undefined){
       var hw= $scope.hwlag
     }
     else{
       var hw= 3
      
     }

var data={'hwlag':hw,'spanewma':sp,'olmean':$scope.outlierwithmean,brand:br,plag:pp,dlag:dd,qlag:qq,'filtervalue':$scope.product1,'date':$scope.datecol,'dateformat':$scope.dateformat12,'filtercol':$scope.filtercol,'quantity':$scope.quantitycol}

    $http.post("/compare",data)
      .success(function(response, status, headers, config) {           
        console.log("compare")
      console.log(response)
      $scope.compare=response;
      })

  }



 $scope.prediction = function() {
     
     console.log($scope.myVar);
      if($scope.predictp != undefined){
       var pp1= $scope.predictp
     }
     else{
       var pp1= 3
      
     }
      if($scope.predictd != undefined){
       var dd1=$scope.predictd
     }
     else{
       var dd1= 0
      
     }
      if($scope.predictq != undefined){
       var qq1= $scope.predictq
     }
     else{
       var qq1= 3
      
     }
      if($scope.pspanewma != undefined){
       var sp1= $scope.pspanewma
     }
     else{
       var sp1= 7
      
     }
     if($scope.phwlag != undefined){
       var hw1= $scope.phwlag
     }
     else{
       var hw1= 3
      
     }
     if($scope.period != undefined){
       var duration= $scope.period
     }
     else{
       var duration= 10
      
     }

var data1234={'algo':$scope.myVar,'duration':duration,'hwlag':hw1,'spanewma':sp1,'olmean':$scope.outlierwithmean,'plag':pp1,'dlag':dd1,'qlag':qq1,'filtervalue':$scope.product1,'date':$scope.datecol,'dateformat':$scope.dateformat12,'filtercol':$scope.filtercol,'quantity':$scope.quantitycol}

    $http.post("/prediction",data1234)
      .success(function(response, status, headers, config) {           
        console.log("predicct")
      console.log(response.graphdata)
      $scope.predicted=response;
      $scope.multi=response.graphdata;
      })

       nv.addGraph(function() {
           var chart = nv.models.lineChart()
          .x(function(d) { return d[0]})
          .y(function(d) { return d[1] })
          .options({
          transitionDuration: 300,    // This should be duration: 300
          useInteractiveGuideline: true
          });
          chart.xAxis.tickFormat(function(d) {
          return d3.time.format('%d/%b/%y')(new Date(d))
          });
          chart.yAxis.tickFormat(d3.format(',.2f'));
          d3.select('#chartforecast svg')
          .datum(cumulativeTestDataforecast())
          .call(chart);
          nv.utils.windowResize(chart.update);

          //TODO: Figure out a good way to do this automatically
          return chart;
      });
      
      function cumulativeTestDataforecast() {
          var data1= $scope.multi;
          return data1        
      }

  }

  $scope.refreshCharts = function () {
     
         $scope.getchart() ;
         $scope.getchart() ;
      
     
  }



$scope.getchart = function(){  

   if($scope.brandname != undefined){
       var br=$scope.brandname
     }
     else{
       var br= 'AM SURGICAL'
      
     }
      if($scope.p != undefined){
       var pp= $scope.p
     }
     else{
       var pp= 3
      
     }
      if($scope.d != undefined){
       var dd=$scope.d
     }
     else{
       var dd= 0
      
     }
      if($scope.q != undefined){
       var qq= $scope.q
     }
     else{
       var qq= 3
      
     }
      if($scope.spanewma != undefined){
       var sp= $scope.spanewma
     }
     else{
       var sp= 7
      
     }
     if($scope.hwlag != undefined){
       var hw= $scope.hwlag
     }
     else{
       var hw= 3
      
     }
  
     var data={'hwlag':hw,'spanewma':sp,'olmean':$scope.outlierwithmean,brand:br,plag:pp,dlag:dd,qlag:qq,'filtervalue':$scope.product1,'date':$scope.datecol,'dateformat':$scope.dateformat12,'filtercol':$scope.filtercol,'quantity':$scope.quantitycol}
      $http.post("/singlelinechart",data)
          .success(function(response, status, headers, config) {
          $scope.singlelinechart=response;
          console.log("singlelinechart");
          console.log(response);
      })

          var data1={'date':$scope.datecol,'dateformat':$scope.dateformat12,'filtercol':$scope.filtercol,'quantity':$scope.quantitycol,'filtervalue':$scope.product1}
      $http.post("/data",data1)
      .success(function(response, status, headers, config) {   
      console.log("dataaaaaaaaa") ;       
      console.log(response);
      $scope.test=response;
      })

      // $http.post("/compare",data)
      // .success(function(response, status, headers, config) {           
      //   console.log("compare")
      // console.log(response)
      // $scope.compare=response;
      // })
     
      $http.post("/meanandstd",data)
          .success(function(response, status, headers, config) {
          $scope.meanandstd=response;
          console.log("meanandstd");
          console.log(response);
      })
      $http.post("/acf",data)
          .success(function(response, status, headers, config) {
          $scope.acf=response;
          console.log("acf");
          console.log(response);
      })
          $http.post("/pacf",data)
          .success(function(response, status, headers, config) {
          $scope.pacf=response;
          console.log("pacf");
          console.log(response);
      })
      $http.post("/decomposition",data)
          .success(function(response, status, headers, config) {
          $scope.decomposition=response;
          console.log("decomposition");
          console.log(response);
      })


      nv.addGraph(function() {
           var chart = nv.models.lineChart()
          .x(function(d) { return d[0]})
          .y(function(d) { return d[1] })
          .options({
          transitionDuration: 300,    // This should be duration: 300
          useInteractiveGuideline: true
          });
          chart.xAxis.tickFormat(function(d) {
          return d3.time.format('%d/%b/%y')(new Date(d))
          });
          chart.yAxis.tickFormat(d3.format(',.2f'));
          d3.select('#chart1 svg')
          .datum(cumulativeTestData1())
          .call(chart);
          nv.utils.windowResize(chart.update);

          //TODO: Figure out a good way to do this automatically
          return chart;
      });
      
      function cumulativeTestData1() {
          var data1= $scope.singlelinechart;
          return data1        
      }
      
         nv.addGraph(function() {
          var chart = nv.models.lineChart()
          .x(function(d) { return d[0]})
          .y(function(d) { return d[1] })
          .options({
          transitionDuration: 300,    // This should be duration: 300
          useInteractiveGuideline: true
          });
          chart.xAxis.tickFormat(function(d) {
          return d3.time.format('%d/%b/%y')(new Date(d))
          });
          chart.yAxis.tickFormat(d3.format(',.2f'));
          d3.select('#chart2 svg')
          .datum(cumulativeTestData2())
          .call(chart);
          nv.utils.windowResize(chart.update);

          //TODO: Figure out a good way to do this automatically
          return chart;
      });
         nv.addGraph(function() {
          var chart = nv.models.lineChart()
          .x(function(d) { return d[0]})
          .y(function(d) { return d[1] })
          .options({
          transitionDuration: 300,    // This should be duration: 300
          useInteractiveGuideline: true
          });
          chart.xAxis.tickFormat(function(d) {
          return d3.time.format('%d/%b/%y')(new Date(d))
          });
          chart.yAxis.tickFormat(d3.format(',.2f'));
          d3.select('#chart3 svg')
          .datum(cumulativeTestData3())
          .call(chart);
          nv.utils.windowResize(chart.update);

          //TODO: Figure out a good way to do this automatically
          return chart;
      });
          nv.addGraph(function() {
          var chart = nv.models.lineChart()
          .x(function(d) { return d[0]})
          .y(function(d) { return d[1] })
          .options({
          transitionDuration: 300,    // This should be duration: 300
          useInteractiveGuideline: true
          });
         chart.xAxis.tickFormat(d3.format(',.0f'));

          chart.yAxis.tickFormat(d3.format(',.2f'));
          d3.select('#chart4 svg')
          .datum(cumulativeTestData4())
          .call(chart);
          nv.utils.windowResize(chart.update);

          //TODO: Figure out a good way to do this automatically
          return chart;
      });
           nv.addGraph(function() {
          var chart = nv.models.lineChart()
          .x(function(d) { return d[0]})
          .y(function(d) { return d[1] })
          .options({
          transitionDuration: 300,    // This should be duration: 300
          useInteractiveGuideline: true
          });
         chart.xAxis.tickFormat(d3.format(',.0f'));

          chart.yAxis.tickFormat(d3.format(',.2f'));
          d3.select('#chart5 svg')
          .datum(cumulativeTestData5())
          .call(chart);
          nv.utils.windowResize(chart.update);

          //TODO: Figure out a good way to do this automatically
          return chart;
      });


       function cumulativeTestData2() {
          var data1= $scope.meanandstd;
          return data1        
      }
      function cumulativeTestData3() {
          var data1= $scope.decomposition;
          return data1        
      }
       function cumulativeTestData4() {
          var data1= $scope.acf;
          return data1        
      }
      function cumulativeTestData5() {
          var data1= $scope.pacf;
          return data1        
      }
      
    
    }

    
}]);
