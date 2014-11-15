function get_tmax(data) {
  var tvl = d3.max(data.vl, function(d) { return d[0]; });
  var tcc = d3.max(data.cc, function(d) { return d[0]; });
  return d3.max([tvl, tcc]);
}

function get_ymax(data) {
 return d3.max(data, function(d) { return d[1]; });
}

function update(data, id) {

 var colors = {"vl": "black", "cc": "steelblue"};

 var div_width = $('.svg-container').width();

 var margin = {top: 10, right: 80, bottom: 60, left: 80},
     width = 0.9 * div_width - margin.left - margin.right,
     height = 500 - margin.top - margin.bottom;

 var tmax = get_tmax(data);
 var vlmax = get_ymax(data.vl);
 var ccmax = get_ymax(data.cc);

 var y_vl = d3.scale.log()
      .domain([40, 1.1 * vlmax])
      .range([height, 0]);

 var y_cc = d3.scale.linear()
      .domain([0, 1.1 * ccmax])
      .range([height, 0]);

 var y = {"vl": y_vl, "cc": y_cc};
 
 var x = d3.scale.linear()
      .domain([0, 1.1 * tmax])
      .range([0, width]);

 var xAxis = d3.svg.axis()
     .scale(x)
     .orient("bottom");
 
 var xAxisTop = d3.svg.axis()
     .scale(x)
     .orient("bottom")
     .tickFormat("");
 
 var yAxis_vl = d3.svg.axis()
     .scale(y_vl)
     .orient("left");

 var yAxis_cc = d3.svg.axis()
     .scale(y_cc)
     .orient("right");

 var chart_ext = d3.select("."+id)
     .attr("width", width + margin.left + margin.right)
     .attr("height", height + margin.bottom + margin.top);

 var chart = chart_ext.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

 chart.append("g")
      .attr("class", "d3-axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .append("text")
      .attr("x", width / 2)
      .attr("y", 50)
      .style("text-anchor", "middle")
      .text("Time from infection [days]");

 // Draw the x Grid lines
 chart.append("g")
     .attr("class", "grid")
     .attr("transform", "translate(0," + height + ")")
     .call(make_x_axis()
         .tickSize(-height, 0, 0)
         .tickFormat("")
     );

 chart.append("g")
      .attr("class", "d3-axis")
      .call(xAxisTop);

  
 var vlTextBox = chart.append("g")
      .attr("class", "d3-axis")
      .call(yAxis_vl)
      .append("g")
      .attr("class", "d3-axis-textbox")
      .attr("transform", "rotate(-90)");

 vlTextBox.append("text")
      .attr("dy", "-4.8em")
      .attr("x", -height / 2)
      .style("text-anchor", "middle")
      .text("Viral load [copies/ml]");
 
  vlTextBox.append("circle")
      .attr("class", "circles vlAxis")
      .attr("cy", "-5.1em")
      .attr("cx", -0.75 * height)
      .attr("r", 7)
      .style("fill", colors.vl);

 var ccTextBox = chart.append("g")
      .attr("class", "d3-axis")
      .attr("transform", "translate(" + width + " ,0)")
      .call(yAxis_cc)
      .append("g")
      .attr("class", "d3-axis-textbox")
      .attr("transform", "rotate(+90)");

 ccTextBox.append("text")
      .attr("dy", "-4em")
      .attr("x", height / 2)
      .style("text-anchor", "middle")
      .text("CD4+ counts [copies/ml]");

 ccTextBox.append("rect")
      .attr("class", "circles ccAxis")
      .attr("y", "-4.8em")
      .attr("x", 0.2 * height)
      .attr("width", 14)
      .attr("height", 14)
      .style("fill", colors.cc);

 chart.append("g")
      .attr("class", "circles VL")
      .selectAll()
      .data(data.vl)
      .enter()
      .append("circle")
      .attr("class", "circle")
      .attr("cx", function(d) { return x(d[0]); })
      .attr("cy", function(d) { return y_vl(d[1]); })
      .attr("r", 6)
      .style("fill", colors.vl)
      .on("mouseover", function(d) { moverDots("vl", d); })
      .on("mouseout", function(d) { moutDots("vl", d); });

 chart.append("g")
      .attr("class", "circles CC")
      .selectAll()
      .data(data.cc)
      .enter()
      .append("rect")
      .attr("class", "rect")
      .attr("x", function(d) { return x(d[0]) - 3; })
      .attr("y", function(d) { return y_cc(d[1]) - 3; })
      .attr("width", 12)
      .attr("height", 12)
      .style("fill", colors.cc)
      .on("mouseover", function(d) { moverDots("cc", d); })
      .on("mouseout", function(d) { moutDots("cc", d); });

 function moverDots(dtype, d) {
     chart.append("path")
         .attr("class", "data-line-" + dtype)
         .attr("d", lineFunction(data[dtype], y[dtype]))
	 .style("stroke-width", 2)
	 .style("stroke", colors[dtype])
	 .style("opacity", 0.3)
	 .style("fill", "none");
 }

 function moutDots(dtype, d) {
   chart.selectAll(".data-line-" + dtype)
        .remove();
 }

 function lineFunction(data, yscale) {
  return d3.svg.line()
            .x(function(d) { return x(d[0]); })
            .y(function(d) { return yscale(d[1]); })
            .interpolate("monotone")(data);
 }

 
 // function for the x grid lines
 function make_x_axis() {
     return d3.svg.axis()
         .scale(x)
         .orient("bottom");
 }

}
