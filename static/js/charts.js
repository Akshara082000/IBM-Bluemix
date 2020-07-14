

'{% if ERROR_MSG == "Found" %}'

var data = JSON.parse('{{ data | tojson | safe}}');
var data = [{
  values: [data['Positive'],data['Negative']],
  labels: ['positive','negative'],
  type: 'pie'
}];

var layout = {
  height: 400,
  width: 500,
  paper_bgcolor: "#161616",
};

Plotly.newPlot('graph1', data, layout);


 /** Function to display gauges  */

 var data = JSON.parse('{{ data | tojson | safe}}');
 var pos=data['Positive']
 var data = [
    {
       type: "indicator",
       mode: "gauge+number+delta",
       value: pos,
title: { text: "Positive Tweets Percentage", font: { size: 24 } },
delta: { reference: 100, increasing: { color: "RebeccaPurple" } },
gauge: {
axis: { range: [null, data['Tweets']], tickwidth: 1, tickcolor: "#3366cc" },
bar: { color: "#3366CC" },
bgcolor: "white",
borderwidth: 2,
bordercolor: "gray",
steps: [
{ range: [0, 50], color: "cyan" },
{ range: [50, 100], color: "cyan" }
],
threshold: {
line: { color: "red", width: 4 },
thickness: 0.75,
value: 90
}
}
}
];

var layout = {
width: 400,
height: 300,
margin: { t: 25, r: 25, l: 25, b: 25 },
paper_bgcolor: "#161616",
font: { color: "#3366CC", family: "Arial" }
};

Plotly.newPlot('posgauge', data, layout);


var data = JSON.parse('{{ data | tojson | safe}}');
var neg=data['Negative'];
var data = [
   {
      type: "indicator",
      mode: "gauge+number+delta",
      value: neg,
title: { text: "Negative Tweeets Percentage", font: { size: 24 } },
delta: { reference: 100, increasing: { color: "RebeccaPurple" } },
gauge: {
axis: { range: [null, 100], tickwidth: 1, tickcolor: "#3366cc" },
bar: { color: "#3366CC" },
bgcolor: "white",
borderwidth: 2,
bordercolor: "gray",
steps: [
{ range: [0, 50], color: "cyan" },
{ range: [50, 100], color: "cyan" }
],
threshold: {
line: { color: "red", width: 4 },
thickness: 0.75,
value: 90
}
}
}
];

var layout = {
width: 400,
height: 300,
margin: { t: 25, r: 25, l: 25, b: 25 },
paper_bgcolor: "#161616",
font: { color: "#3366CC", family: "Arial" }
};

Plotly.newPlot('neggauge', data, layout);

        
             let values=[]
             var count=0
             let freq=[]
            '{% for key,values in words.items() %}'
                
                    if(count!=30){
                       values.push('{{values}}')
                       count=count+1;
                    }
            '{% endfor %}'
            count=0
            '{% for key,values in freq.items() %}'
                
                if(count!=30){
                   freq.push('{{values}}')
                   count=count+1;
                }
        '{% endfor %}'

            console.log(values);
            console.log(freq)
            $(document).ready(function(){
                var entries= values.map(x => ({label:x,url:"https://twitter.com/search?q="+x}));
                var settings = {
                    entries :entries,
                    width:640,
                    height:400,
                    radius:'85%',
                    radiusMin:75,
                    bgDraw:true,
                    bgColor:'#161616',
                    opacityOver:1.00,
                    opacitySpeed:6,
                    fov:800,
                    speed:2,
                    fontFamily:'Courier,Arial,sans-serif',
                    fontSize:'30',
                    fontColor:'white',
                    fontWeight:'bold',
                    fontStyle:'normal',
                    fontToUppercase:true,
                };
                $('#graph3').svg3DTagCloud(settings)
            });
           
            var data = [
                  {
                     x: values,
                     y: freq,
                     type: 'bar',
                     bgcolor: "black",
                  }
              ];
            
              var layout = {
                      width: 800,
                      height: 400,
                      paper_bgcolor: "#161616",
                      
                      font: { color: "white", family: "Arial" }
                  };
      Plotly.newPlot('graph4', data,layout);
      '{%endif%}'
      