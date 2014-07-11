/* Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License. */

    var GRID_SIZE = Math.floor((Math.random() * 40) + 3); // Size of the grid.
    var GRID_INDEX = GRID_SIZE - 1; // Max index for the grid.
    var MAX_N = Math.floor((Math.random() * GRID_SIZE) + 2);
    var MAX_IT = Math.floor((Math.random() * GRID_SIZE) + 2);
    
    // additional offsets    
    var X0 = 0;
    var Y0 = 0;
    
    // to be loaded dynamically for each SVG
    var svg = null;
    var svgNS = '';
    var area = null;
    var GX_SIZE = 10;                       // DEFAULT pixels per node.
    var MAX_R = Math.floor(GX_SIZE / 2);    // DEFAULT Maximum node radius (px).

    $(document).ready(function(){

        $(".svg-logo")
            .on("click", __drawLogo());

    });

    function __drawLogo()
    {
    
        if ( __DEBUG__ ) console.log("drawLogo!");
    
        initSVG();
        drawGrid();
        
    }
    
    function initSVG()
    {
    
        svg = document.getElementById('svg-logo');              
        svgNS = svg.namespaceURI;
        area = document.getElementById('svg-area');
        
        var c = document.getElementById('svg-container');
        var w = c.getAttribute('width').replace('px', '');
        
        GX_SIZE = Math.floor(w / GRID_SIZE);
        MAX_R = Math.floor(GX_SIZE / 2);
        
        if ( __DEBUG__ )
            console.log('w = ' + w 
                            + ', GRID_SIZE = ' + GRID_SIZE
                            + ', GX_SIZE = ' + GX_SIZE 
                            + ', MAX_R = ' + MAX_R 
                            + ', MAX_IT = ' + MAX_IT);

    }
                        
    function drawGrid()
    {
     
        for ( var k = 0; k < MAX_N; k++ )
        {
        
            var i = Math.floor((Math.random() * GRID_SIZE));
            var j = Math.floor((Math.random() * GRID_SIZE));
            
            drawNode(i, j);
            
            var pi = i; // parents
            var pj = j;
            
            // more siblings?
            for ( var l = 0; l < MAX_IT; l++ )
            {
                
                var s = Math.floor((Math.random() * 8) + 1);
                if ( s == 0 ) { continue; }
                
                var ii = pi - 2 + ( s % 3 );
                var jj = pj - 2 + ( Math.ceil( s / 3 ) );
                
                if ( ( ii < 0 ) || ( ii > GRID_INDEX ) ) { continue; }
                if ( ( jj < 0 ) || ( jj > GRID_INDEX ) ) { continue; }
                
                drawNode(ii, jj);
                drawLine(pi, pj, ii, jj, '1');
                
                // this sibling is now the parent...
                pi = ii;
                pj = jj;
            }

        }

    }
               
    function drawLine(pi, pj, ii, jj, w)
    {
        var x1 =  Math.floor(pi * GX_SIZE) + X0;
        var y1 =  Math.floor(pj * GX_SIZE) + Y0;
        var x2 =  Math.floor(ii * GX_SIZE) + X0;
        var y2 =  Math.floor(jj * GX_SIZE) + Y0;
        addLine(x1, y1, x2, y2, w);
    }
    
    function addLine(x1, y1, x2, y2, w)
    {
        var e = document.createElementNS(svgNS, 'line');
        e.setAttribute('x1', x1);
        e.setAttribute('y1', y1);
        e.setAttribute('x2', x2);
        e.setAttribute('y2', y2);
        e.setAttribute('fill','white');
        e.setAttribute('stroke','white');
        e.setAttribute('stroke-width', w + 'px');
        e.setAttribute('stroke-opacity','1.0');
        area.appendChild(e);
    }

    function drawNode(i, j)
    {
        var r = Math.floor((Math.random() * MAX_R) + 1);
        var x = Math.floor(i * GX_SIZE) + X0;
        var y = Math.floor(j * GX_SIZE) + Y0;
        addNode(x, y, r);
    }
           
    function addNode(x, y, r)
    {
        var e = document.createElementNS(svgNS, 'circle');
        e.setAttribute('cx', x);
        e.setAttribute('cy', y);
        e.setAttribute('r', r);
        e.setAttribute('fill','white');
        e.setAttribute('stroke','white');
        e.setAttribute('stroke-width','1px');
        e.setAttribute('stroke-opacity','1.0');
        area.appendChild(e);
    }

