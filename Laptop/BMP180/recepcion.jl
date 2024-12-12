using Gtk
using Sockets

# Constantes
Po = 1013.25
OSS = 1
glade = GtkBuilder(filename = "Interfaz.glade")

window = glade["window"]

celcius = glade["celcius"]
farenheit = glade["farenheit"]
mbar = glade["mbar"]
inhg = glade["inhg"]
metros = glade["metros"]
foot = glade["foot"]

showall(window)

# Configuracion de sockets
server=listen(IPv4(0),12345)
socket=accept(server)

println("Conexión aceptada: ")
println(getsockname(socket))
println(getpeername(socket))
print("\n")

function calcularTemperatura(cons,ut)
    x1=((ut-cons["AC6"])*cons["AC5"])>>15
    x2=(cons<<11)/(x1+cons["MD"])
    b5=x1+x2
    temp=(b5+8)>>4
end

function calcularPresion(cons,b5,up)
    b6=b5-4000
    x1=(b2*((b6^2)>>12))>>11
    x2=(cons["AC"]*b6)>>11
    x3=x1+x2
    
end

nombres=["AC1","AC2","AC3","AC4","AC5","AC6","B1","B2","MB","MC","MD"]
constantes={}

try
    for i in nombres
        constantes[i]=readline(socket)
    end
    while true
        msg=readline(socket) |> chomp
        @show msg
        if msg=="Adios_garuda"
            close(server)
            print("¡Adios!")
            break
        elseif msg=="Temperatura"
            msg=readline(socket) |> chomp
            b5,t = parse(Int,msg) |> calcularTemperatura
        elseif msg=="Presion"
            msg=readline(socket) |> chomp
            p = parse(Int,msg) |>cal
        #=
        else
            println("Mensaje no reconocido: $msg")
            sleep(0.1) =#
        end
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
