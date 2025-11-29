# Ordering



Then we will upload the files to JLCPCB and the automated system should extract the number of layers as well as the dimensions for this board which it looks like it has. We have this simple board preview. We can check just very roughly if the holes are in order, if the silk screen, solder mask openings, copper top and bottom have been exported correctly.

And we can also use the Gerber viewer to double check that. And I'd strongly suggest checking that because it gives you yet another view on the PCB design, which is always a good thing. In any case, we're using a simple F FR4 two layer board. The dimensions have been correctly identified as 53x 28 mm, and we're just going to get five produced. That's the minimum amount, at least from manufacturing. We're going to use a standard 1.6 mm thick PCB.

That's the default or very common for two-layer PCBs. Green solder mask color and white silk screen. Those options are the quickest, most standard, and cheapest. Surf as finish, I typically at least go with lead free hot air surface leveling. For more complicated boards, if you maybe need a longer shelf life, if you need a flatter surface finish, then you might want to go with enigm nickel gold.

The highspec options we can just keep as default. What I do like to check, however, is the confirm production file option. I want to be in control of what is produced. And the way I can do that is by asking my manufacturer to send back their actual manufacturing files that they're going to be using in production.

And the way I can do that is by clicking yes on here and checking do not confirm automatically. That'll add a small $1 search charge, but I definitely think that's worth it. That would be then enough. You would just have to click on save to cut to get five PCBs that we just designed manufactured. And excluding shipping, tariffs, customs, and so on. That's just over $4 for five PCBs, which I think is incredible.

But we would, of course, want to have our PCBs assembled as well. So, very easily, we just check the PCB assembly option. For us, we just want the top side assembled. There are two different PCBA types, economic and standard. Standard includes more advanced options for assembly and also includes finer pitch parts.

Now, we could use economic in this case because most of our parts are very simple. However, because of the addition of U4, our accelerometer that has a very fine pitch small part, we actually have to use standard assembly. So, you could in your design, if you want to use an accelerometer, maybe choose a package that's easier to assemble and economic PC PCB assembly is a bit cheaper than standard, but standard is pretty affordable as well. So, we go with standard again because we have this fine pitch component.

I would like to just have the top side assembled and that's cheaper, of course, and that's also what we have on our board. We don't have any components on the bottom layer. So top side and we can go anywhere from two to five boards at least. That's because we set five as a maximum because that's what we set for how many boards we want manufactured.

We could of course change that by changing the overall PCB quantity, but for now let's just get five PCBs manufactured. Edge Rails will let JLC PCB add and I would like them to confirm the parts placement with me as well. That's similar to the confirming the production files. Click confirm. The rest we can leave as standard for now and then just click next.

Here we get a little board preview again where we can have a quick look and then click next. Now we need to add our assembly files. So the blue materials in the JLC required format and the component placement or pick and place file again in the JLC required format that we just saw. I selected the blue materials and the component placement file.

Now click process and very quickly JLC's automated system brings you to this page. On the left hand side we can see what was extracted from the blue materials and on the right hand side we can see what the automated system has figured out what we want to have assembled. So we need to go through row by row check is the component on the left actually matched with the component on the right and of course in most cases it is.

But I strongly suggest going through line by line checking is this the component we actually want assembled in the right package and so on. Sometimes there might be not a check mark next to the component. For instance, here we get a little notification that a special component fee of 3 cents per piece will be charged because the processing of this USB connector happens to be difficult.

We can agree to that by just clicking the little select check box on the right hand side and make sure to go through this in detail. But once you're happy with that, we just have to click next. Then we get led to what I think is one of the best parts of using JLCPCB is that we get our footprints are shown to us and we can visually check if the footprints look in order.

We can check the rotations, orientations, placements, and so on. Now, you will already have noticed that some of these components aren't rotated correctly. And this is because every manufacturer, every assembly house, every ECAD tool uses a different orientation standard. So, where is 0°? Is that north, south, east, west? And that becomes of course problematic if everyone uses their different standards.

So pretty much in any case, every time you use a different ECAD tool, depending on how you set up your libraries, you will have to rotate your components in this view. But that's very straightforward. I'm just going to go to 2D view. If we zoom on a component, for example, U1, I click on this and press spacebar and rotate it by 90° each time until it's in the correct orientation. And I'll just do that for the rest of these components. And that's very quick to do, but that's something I would suggest verifying as well.

But again, I really like this view because it lets me check at least very roughly visually that the footprints look somewhat in order. I can do that in 2D, but also in 3D view just by moving my mouse around here. So, I think this is a very cool feature of JLCPCB. You might have also already spotted on the left hand side this little checker chest box mark is because JLCPCB hasn't got the 3D model info there yet.

But once you actually place the order, they will typically generate that info that you can then use for the next time as well. Also, once you've checked the check parts placement, you should get an image or an interactive viewer that actually shows this missing footprint or 3D model. I did notice one thing here. So, this footprint has two pin one indications here, which aren't an alignment.

And that's again another reason why I always check the confirm part placement button because this was probably generated by an automated system at JLCPCB. So, there will be some human involvement to actually check this part. Just make sure you always check that option because things like this can happen.

For instance, if you've checked this and everything looks in order, all the pin one indicators are there, all the footprints look all right, we can then scroll down and click next. But that's pretty much it. Now we get a list of all the charges that are required to produce the printed circuit board as well as to do the assembly.

And overall for five boards excluding shipping, we are just below $80, which I think is pretty incredible because you don't have to do any of the soldering yourself. none of the PCB manufacturing yourself. So I think that's pretty good. We do also have to select what this device is going to be used for and that's just for shipping and customs. So in our case that would be research education and it's just a development board or DIY for instance.

Then you can save to cart and check out using your preferred shipping and payment method. So I think this is pretty good and pretty straightforward. Thank you very much for watching this video and well done for making it through these two videos. I know it's been a long series, but hopefully it's been useful showing you the whole PCB design and schematic design process for simple MSPMO microcontrollerbased board using Keycad 9.
