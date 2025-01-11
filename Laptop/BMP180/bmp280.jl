using Sockets

# Configuracion de sockets
server=listen(IPv4(0),12345)
socket=accept(server)

println("Conexión aceptada: ")
println(getsockname(socket))
println(getpeername(socket))
print("\n")

nombres=["T1","T2","T3","P1","P2","P3","P4","P5","P6","P7","P8","P9"]
constantes=Dict()

function convertirAEntero(dato)
    try
        parse(Int32,dato)
    catch e
        print("No se pudo convertir")
    end
end

function calcularTemperatura(dato,dig)
    adc_T=parse(Int32,dato)
    var1=((adc_T>>3)-(dig["T1"]<<1)*dig["T2"])>>11
    var2=(((((adc_T>>4)-dig["T1"])^2)>>12)*dig["T3"])>>14
    t_fine = var1 + var2
    t = (t_fine*5 + 128)>>8
    return t_fine,t
end

function calcularPresion(dato,t_fine,dig)
    adc_P=parse(Int32,dato)
    var1 = t_fine - 12800
    var2 = ((var1^2)*dig["P6"]) + (var1*(dig["P5"]<<17)) + (dig["P4"]<<35)
    var1 = (((var1^2)*dig["P3"])>>8) + ((var1*dig["P2"])<<12)
    var1 = (((1<<47)+var1)*dig["P1"])>>33
    if var1==0
        return 0
    end
    p = 1048576 - adc_P
    p = div(((p<<31)-var2)*3125,var1)
    var1 = (dig["P9"]*(p>>13)^2)>>25
    var2 = (dig["P8"]*p)>>19
    p = ((p+var1+var2)>>8) + (dig["P7"]<<4)
    return p
end

function obtenerValores(socket,constantes)
    msg=readline(socket) |> chomp
    if msg=="Temperatura"
        msg=readline(socket) |> chomp
        global t_fine,t = calcularTemperatura(msg,constantes)
        # @show t
        temp = t/1000
        println("Temperatura = $temp")
    elseif msg=="Presion"
        msg=readline(socket) |> chomp
        p=calcularPresion(msg,t_fine,constantes)
        # @show p
        press = p/256
        println("Presion = $press")
    else
        @show msg
    end
end

global t_fine

try
    for i in nombres
        constantes[i]=readline(socket) |> (con -> parse(Int32,con))
    end
    @show constantes

    while true
        obtenerValores(socket,constantes)
    end

catch e
    if isa(e,InterruptException)
        println("\nCerraste el programa")
    else
        print("Algo salio mal :(")
        rethrow(e)
    end

finally
    close(socket)
    close(server)
end
