var dataset = [100, 115, 20, 30, 60, 65, 213, 199]

var svgWidth = 500, svgHeight = 300, barPadding = 5, barWidth = (svgWidth / dataset.length) - 1, borderSpacer = 12;

var svg = d3.select('svg')
    .attr('width', svgWidth)
    .attr('height', svgHeight)
    .style('background-color', 'black');

svg.append("text")
    .attr("x", svgWidth / 2)
    .attr("y", 25)
    .attr("text-anchor", "middle")
    .attr("fill", "white")
    .attr("font-size", "18px")
    .text("Matrix");

var barChart = svg.selectAll('rect')
    .data(dataset)
    .enter()
    .append('rect')
    .attr('y', function(d) {
        return svgHeight - d;
    })
    .attr('height', function(d) {
        return d;
    })
    .attr('width', barWidth - barPadding)
    .attr('x', function (d, i) {
        return barWidth * i + borderSpacer / 2;
    })
    .attr('fill', 'white');

svg.selectAll('text')
    .data(dataset)
    .enter()
    .append('text')
    .text(function(d) {
        return d;
    })
    .attr('x', function(d, i) {
        return barWidth * i + borderSpacer / 2 + (barWidth - barPadding) / 2;
    })
    .attr('y', function(d) {
        return svgHeight - d - 5; // 5px above bar
    })
    .attr('text-anchor', 'middle')
    .attr('fill', 'white')
    .attr('font-size', '12px');


    // var text = svg.SelectAll('text')
    // .data(dataset)
    // .enter()
    // .append('text')
    // .text(function(d) {
    //     return d;
    // })
    // .attr('y', function(d, i) {
    //     return svgHeight - d - 2;
    // })
    // .attr('x', function(d, i) {
    //     return (barWidth * i) 
    //     //+ borderSpacer/2 + (barWidth - barPadding)/2;
    // })
    // .attr('fill', 'white')
