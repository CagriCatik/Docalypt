# Routing I2C & UART



Again, because we've done a fairly good job at laying out this board, the routing is fairly straightforward. It's just connecting dots, connecting colorful lines, and so on. So, I'm going to do the I squed C lines first. I'll come out with I squed C at 0.3. Go into the pull-up resist. I'm going to do the same for I squed C SC. Now, we could of course drag the track up a bit.

That gives us a tiny bit more clearance away from the SDA line that they don't run in parallel for too long. Will it make a difference in this case? No. But it's generally good practice. I can't pull the SDA line up too high because remember we have the UARD CTS line there and the RTS line as well.

So that's why I'm deliberately keeping the dent in this line, keeping this 45° segment in this line a bit further down so I have space to escape with RTS and CTS out of the pull-up resistors. Then we need to go into the accelerometer pads. I can already see this V is going to be a bit too close. So let me just move this out of the way for now. I'm going to move this V a bit to the right to give myself a bit of breathing room for SCL.

Let me just move it down a tiny bit. We can fix all this later. X to root. Come out. And you can see we're going to have to neck down again as usual. Now Keycad is actually letting me go in. So I guess this could be okay because we're not overextending the pad. I'm just going to drag this move this segment from the track away from the V a bit more.

And then we can do something similar. Then we do something similar for SDA. Come out. Give myself a tiny bit of space. But here we'll have to neck down. You see keycat is not letting me go into the pad straight away. So again this is just a quick effort. Something like this might be as an okay starting point. You can still fine-tune quite a bit later.

Now we have the interrupt connections as well. So I'm just going to you can either start from the IMU or from the MCU. I'm just going to start from the MCU route out giving myself a bit of clearance. Coming past giving myself clearance from the 3.3 W connections like so. And then of course we have to neck into this again. And for the in two pin we also do the same thing.

I don't want to hug the traces like so. I don't want to do something like this. Just using the absolute minimum clearance. I do want to give myself some clearance. Again will it make a difference in this case? Probably not. But cross talk can and is a real issue in PCB design. So that's why the the number one thing you can do to minimize cross talk is actually increase spacing.

So that's exactly what we're trying to do here. And then we have to neck down into that pad again. For instance, something like this. Now I also want to move my int 2 trace up a bit this horizontal segment because you can see the ground plane underneath. It's pretty close to the edge for my liking.

So, you don't want your traces to be close to the edge of the reference planes because then you get kind of field spread extending beyond the board. That isn't great for EMI. So, I'm going to move it a tiny bit up. Now, there's not terribly much we can do. Of course, we could move all of these components up a bit more or move this whole segment up a bit more, but for now, this is okay.

We will have to find a way to jumper the 3.3 volt nets later on, but just as a simple example of what you could do to fan out and route out this I squed C connection. They're not terribly critical sections, but we because of the way we've laid this out, we can keep these connections fairly short, fairly simple. We don't really have any crossings we have to do with VAS, at least for the moment.

So, we've pretty much done all of the MCU part. All that is left signal-wise are the UA connections. And hopefully, we've done a fairly okay job again for layout. Because here, URX, U RX, we can simply route out with a 0.3 mm trace width. I'm going to go up a bit. I'm actually going to give myself a bit of space away from the 3.

3 volt pad because I'm probably going to want to place a V here because I can't really get to this capacitor any other means. I could go under the MCU, but we'll see later how to properly route power. And we we want to go through the decoupling capacitor first before we go into the MCU pad. So, I'm going to route this way.

I'm This is just indicative that I need to properly put a via here. UX I'm going to do as well. And I'm not going to hug the traces again. I'm going to come out and try and break away quickly. give myself some space and route into the TX pad. And again, I can always make adjustments later simply by dragging. Make sure to keep fairly nice pad entries like so.

Give yourself spacing between the various traces as well. So, you know, something like this seems to be fairly in order. A possible option for the 3.3 actually might be through this capacitor, through the pad, then into this capacitor for the MCU. But that's just thinking ahead a tiny bit. Okay, so now we have CTS RTS. Let's see how we need to connect them. And it seems actually fairly straightforward.

I don't think we actually have to do any crossing. We just come RTS out here below the crystal up into RTS and CTS. We can come out the left side and then go under the RTS trace. So that's exactly what we're going to do. Let me just drag this SDA trace down a bit. Press X 0.3 m trace width. Come out past these pull-up resistors.

Give myself ample space away from the crystal oscillator. And I'm going to come into let me just move this grand via a tiny bit. We we'll probably move this around a bit more afterwards as well. It's just I didn't have really space to move the CTS signal in properly. Now for the RT signal, very similar.

Come out, give myself space immediately when I come out of the pad. I don't want them hugging. Now I can either move it close to the crystal or the crystal capacitor here or I can move it closer and kind of hugging the UR connection. In this case, what do you do? You can place it centrally and that's kind of the I don't know worst of both worlds.

I prioritize that I want to stay away from the crystal. That's why I'm going to move the trace closer to the CTS line until I can break away and have ample space from the crystal. That's a exactly the reason I place this via fence for lack of a better word around the crystal to tell myself, okay, I can't go close to the crystal here.

I'm going to go around and I'm going to have a nice pad entry like so. I could also come into the pad like this. I prefer having this kind of horizontal entry like so. For RF designs, that can sometimes make a difference how you enter the pad, but for us, it doesn't really matter terribly much. I do want to give myself a tiny bit more spacing because we have fairly long parallel runs.

Again, will it matter? Probably not, but it's a matter of doing and following good practices. Again, staying away from the crystal and just adjusting and correcting a tiny bit. For instance, something like this. I'm giving my space when I can have space. I'm trying to stay away from the crystal, but I'm also trying to minimize or reduce the length of trace I have generally because you want to reduce the length of traces.

It reduces the chance of this becoming an unintentional radiator, also known as an or an antenna. And the way we can do that is by keeping our trace length as short as is reasonable for this board design. But this seems fairly good. The nice thing is we still on the bottom layer have an unbroken for the most part solid ground plane. We try and only route on the top layer and only do small jumps. So we might have to do some small jumps on the bottom layer later on.

We've connected up most of the MCU connections, of course, not power and ground, but now we can move more to the left hand side and finish off essentially with the USB signals before we move over to the power routting. And then we're really pretty much done and ready to check the board of course and then produce manufacturing files for ordering.
