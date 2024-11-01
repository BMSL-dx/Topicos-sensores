using Gtk
using Sockets

# Constantes
Po = 1013.25

glade = GtkBuilder(filename = "Interfaz.glade")

window = glade["window"]

celcius = glade["celcius"]
farenheit = glade["farenheit"]
mbar = glade["mbar"]
inhg = glade["inhg"]
metros = glade["metros"]
foot = glade["foot"]

showall(window)

server=listen(IPv4(0),12345)
socket=accept(server)

println("Conexión aceptada: ")
println(getsockname(socket))
println(getpeername(socket))
print("\n")

function altura(p)
    return 44330*((p/Po)^(1/5.255))
end

function celcius_farenheit(temp)
    return 1.8*temp + 32
end

function mbar_inhg(p)
    return p*0.0295299830714
end

function metros_foots(alt)
    return atl*3.28084
end

try
    while true
        msg_inicial=readline(socket)
        #println(msg)
        msg=chomp(msg_inicial)
        if msg=="Adios_garuda"
            close(server)
            print("¡Adios!")
            break
        elseif msg=="Temperatura"
            msg_inicial=readline(socket)
            msg=chomp(msg_inicial)
            # println(msg)
            GAccessor.text(celcius,msg)
        elseif msg=="Presion"
            msg_inicial=readline(socket)
            msg=chomp(msg_inicial)
            #println(msg)
            GAccessor.text(mbar,msg)
        elseif msg=="Altura"
            msg_inicial=readline(socket)
            msg=chomp(msg_inicial)
            #println(msg)
            GAccessor.text(metros,msg)
        elseif msg=="Temp2"
            msg_inicial=readline(socket)
            msg=chomp(msg_inicial)
            #println(msg)
            GAccessor.text(farenheit,msg)
        elseif msg=="Pres2"
            msg_inicial=readline(socket)
            msg=chomp(msg_inicial)
            #println(msg)
            GAccessor.text(inhg,msg)
        elseif msg=="Alt2"
            msg_inicial=readline(socket)
            msg=chomp(msg_inicial)
            #println(msg)
            GAccessor.text(foot,msg)
        else
            println("Mensaje no reconocido: $msg")
            sleep(0.1)
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


