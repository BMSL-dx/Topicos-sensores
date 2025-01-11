/*translate([-27,0,25])
    cube([5,50,50],center=true);

translate([27,0,25])
    cube([5,50,50],center=true);
    
translate([0,0,2.5])
    cube([50,50,5],center=true);*/
    
module caja(espesor=5,largo=50,ancho=50,altura=50){
    difference(){
        cube([largo,ancho,altura]);
        
        translate([espesor,espesor,2*espesor])
            cube([largo-2*espesor,ancho-2*espesor,altura]);
    }
}

module respirar(espesor=5,largo=50,ancho=50,altura=50){
    n=ancho/(2*espesor+1);
    for(i = [1 : 1: n]){
        translate([0,i*(2*espesor),2*espesor]){
        cube([largo+2*espesor,(5/4)*espesor,altura-3*espesor]);
        }
    }
}

module dona(altura=20,diam_ext=6,diam_int=2){
    difference(){
        cylinder(altura,d=diam_ext,$fn=100);
        translate([0,0,(altura/2)+5])
        cylinder(altura/2,d=diam_int,$fn=30);
    }
}

module jaula(){
    difference(){
        caja();
        
        translate([-2.5,-2.5,0])
        union(){
            translate([55,0,0])
            rotate([0,0,90])
                respirar();
            
                respirar();
        }
    }
}

union(){
    jaula();
    
    translate([25,25,0])
    dona(altura=30,diam_ext=8.5,diam_int=3);
}
/*union(){
    translate([55,0,0])
    rotate([0,0,90])
        respirar();
    
        respirar();
}*/