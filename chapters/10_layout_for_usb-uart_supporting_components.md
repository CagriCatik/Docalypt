# Layout for USB-UART Supporting Components



What we want to do now is maybe move to the next critical thing. Of course, power is critical as usual, but that's something I might do a bit last unless I have a lot of, for example, switching converters or high frequency switching converters. A lot of them, lot of different rails. I also have to pre-plan that a bit better. But for now, the next critical thing seems to be U2, which is a USB to converter because this has a somewhat fast USB interface and it has a various different connections.

Going back to the schematic, looking at U2, what does it need? Okay, it's got power and ground connections, but expounding circuitry, it's only really C6 and C7. And the way we place these capacitors is again because they are decoupling capacitors. We want to place them close to the relevant power and of course ground pins. That's pin 7. And that we want to have adjacent to C6 and pin 10 is what we want to have adjacent to C7.

There's a reason why I've placed my capacitors like this on the schematic. And this is an indication to whoever does the PCB design, this is the order I want them. I don't want C6 next to pin 10, and I don't want C7 next to pin 7. I want C6 next to pin 7 and C7 next to pin 10, just as it is with the schematic. It's delivering design intent.

Now, you might say, okay, this isn't really important. They're both the same voltage. They're both the same capacitor. It doesn't really matter, which is in this case absolutely correct, but it's a matter of principle. It's a matter of following through even in the most basic of boards that you can do those for more advanced designs as well.

So, with that being said, take C6 and let's put it next to pin 7. Pin 7 of U2. And that happens to be right here. So this is a bit of a squeeze at the moment. I could rotate the capacitor like so. Means we have a fairly close connection to pin 7 which is exactly what we wanted. However, our ground needs will need to be connected somehow and we're interfering with UR0 TX and UR0 RX.

Before we could simply route out pins 9 and 8 into pins 1 2 of the mic controller. But placing this capacitor here, yeah, that isn't that great. What we could do instead is take this capacitor and sacrifice do a compromise and move the capacitor for instance somewhere like here. We would then route power through the capacitor and then neck down the trace into pin 7.

This then gives us clearance to route out TX and RX pins. Okay, it's less optimal than the closer connection. But in this case, this is also a reasonable attempt of doing this connection and it means we need less VS or jumps or hoops to route out TX and RX. Again, this is a matter of experience knowing when and when you can't do these things.

But the simpler the circuit, the lower the speeds in your design. Typically, you can get away with this more and more. Now, we had the other capacitor that was C7 and we said they want that next to pin 10. Let's take C7 and we can move that next to pin 10. Again, we have various options. We could place like so where we have the same problem as before.

We can place it like so, which gives the shorter connection, but we also have to keep the ground connection in mind. So what we could do also for the sake of symmetry is take that capacitor and have it symmetrically similar to C6. Again, we still have a fairly short connection between pin pad one of the capacitor and pin 10 of our USB to converter. And we've made it look a tiny bit aesthetic.

Not that that's terribly important, but I find a nice PCB layout is something very nice to look at. And in any case, this might be an appropriate positioning of these decoupling and bypass capacitors. So let's just move the silk screen out of the way as usual. Something like this might be completely fine to do. Again, keeping in mind current loops, power paths, short connections, as we'll see later.

And we're just trying to facilitate an easier time when it comes to routting later on. We don't have terribly many components left. Let me just drag all of these over just a tiny bit just so I don't always have to scroll to the right all the time. Looking at the schematic, what do we have left? We have our accelerometer, of course, so that might be the next critical thing.
