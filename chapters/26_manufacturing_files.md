# Manufacturing Files



that will be typically in a Goba file format, although that's kind of outdated these days, but a lot of the more affordable PCB manufacturing houses don't really support OW++ or the IPC based file format just yet. So, we'll just stick with Gerber. That would be enough to get your board manufactured.

If you want to assemble it at home by yourself, that would be all you would need, but we would like to get this assembled. In my particular case, I'd like to go with JLC PCB where I had the actual demo boards manufactured and assembled. So, we also need a bit of materials.

So what components are on this board? Where can we source them from? What are their names? What are the manufacturers? And we need a pick and place or component placement file. And that tells the the assembler relative to a certain origin. In this case, we have the bottom left. What are the coordinates of the centers of the components for the microcontroller center, the diode centers, the capacitor centers, as well as their relative orientation. So rotation.

So these three files or sets of files is what we need to produce to get this board manufactured and assembled. Now the process is fairly straightforward specifically for Gerbers. We can just go to the top left file fabrication outputs Gerbers. Here we want to select the output directory and I'll just select my root directory of my project.

Then create a new folder and just call it manufacturing or MFR for short. Choose this folder. We can use a relative path. That's okay. Then we need to select what layers we want. We definitely want the front and bottom copper layers. We want the front paste. We are not using the bottom paste. There are no components on the bottom paste. We want the front silk screen. We have no silk on the bottom.

We want the front mask, solder mask, and we the bottom mask. And we want the edge cuts, which is our outline layer. We want to use the extended X2 format. We want to use the drill place file origin. And we're going to uncheck indicate do not place on fabrication layers. Not that for this project, this actually means terribly much. We don't need a go job file for this particular manufacturer.

So, we're going to uncheck that. Once we've selected these options, then we can just have to click on plot on the bottom right that button. We can see the exported files in our manufacturing folder where we have the front copper, bottom copper, front mask, bottom mask, a front pace layer, silk screen, and of course, our outline, which is our edge cuts layer.

Other than those Gerber files, we of course have drills in our design. both plated throughhole drills, PTH, and non-plated throughhole drills, which happen to be part and loose in this design of the TAC Connect TC2030 programming header. To plot those or generate those drill files, we just click on the generate drill files button on the bottom right output folder.

We select the same as we do with the Gerber files under manufacturing. I'd like to use a pretty standard format for this is the Exelon drill file format rather than Gerber, but check with your manufacturer what files they would like to see. We can leave these options as default on the right hand side.

We would like to use the drill place file origin units millimeters in our case and we'll stick with the decimal format for the amount of zeros. Then click generate. We can close that and we can see in our manufacturing folder again we have now in addition PTH plated through hole and NPTH non-plated throughhole drill files. And these sets of files compromise the Gerber files.

In our case we just need to zip them up into an archive. So zip or raw archive. And that's exactly what I've done here. just created a simple zip archive and that's going to be our gober archive. The GABA files are of course enough if you just want to have your PCB manufactured without assembly. For instance, if you want to assemble the parts at home by yourself.

If you do want assembly, we do need to provide two more files as an absolute bare minimum. And this is the component placement file or pick and place file which tells the manufacturer the assembler relative to a given origin where are the centers of the various components where the X and Y coordinates for example for the microcontroller.

What's the rotation of the microcontroller? All of that is contained in the pick and place file. Other than that, we of course also need a bit of materials which tells the manufacturer what components are on the board, what their reference designators are, where to source them from, and so on. First of all, while we're still in the PCB design view, we can export the pick and place file.

If you go to the top left file, fabrication outputs, and then component placement file. We'll do units, millimeters, format CSV, and we can keep the rest as default and click on generate position file. This really depends on your manufacturer and assembler.

But for instance, GLC PCB can be very picky of what their automated system detects as a an adequate pick and place file. For instance, they provide this reference here. So you need a designator mid X, mid Y, layer and rotation and the format pretty much identically to how it is here. This could be an Excel file, it could be a CSV file and so on.

You have to have the right columns however and the right structure for the system to detect it unfortunately. So this is what Keycad exports. You can see it's not entirely the format that JLC PCB wants. So I've adapted it to the format JLCPCB wants. It's pretty much just changing the header to designator value, footprint, midex, bit, y, rotation, and layer.

And sometimes when JLCPCB throws an error, you might just need to put quotation marks around the various fields in your CSV file. I know it's irritating, but unfortunately this has to be done to work with the JCPCB assembly. Then to export the bill of materials, we move back over to the schematic. And remember for all of these schematic symbols, we while we were creating the schematic, we entered the relevant information as symbol fields. And we can check that by going to the top in edit symbol fields.

We can see that we have the reference designator. We have the quantity value, what footprint we're using, but also the additional fields we added such as manufacturer, manufacturer part number, various distributor links, as well as the LCSC part number, which comes into play if you'd like to get your boards assembled at JLCPCB. And we filled in this information as we went along.

And I strongly suggest you generate your libraries with this information in place so you don't have to keep re-entering and re-entering it. Also from the last video um while I was going through also a comment by Derek also highlighted that I picked out the wrong package type at least the part number for the 470 nanopharad 063 capacitor I actually picked at 085 then selected a different manufacturer part number just to correct that which is an 063 470 nanofharad capacitor.

So hopefully all of this should be okay but please keep in mind we all need to check our bill of materials. There's a lot of human error that can come into this. In any case, once you have the information in place, all you have to do is click export and it's actually written to the root folder. And this is what the bill of materials export then looks like.

I did adjust the top header designator used to be reference with the Keycat export and quantity used to be QTY. So I've just expanded that just to make JCPs be happy. The rest is exactly as Keycat exported it. So these are the three folds we then need as an absolute bare minimum to get our board manufactured and our boards assembled as well. If you just want to get your boards manufactured, again, you just need the Gerber archive.

If you want them assembled on top of that, we need the bill of materials as well as the pick and place file. So now, let's move over to JLCPCB and see how we can order these. Here we now are at jlcpcb.com. And all we have to do is click on instant quote. Then we need to upload our Gerber files. So click on add Gerber file. Select our Gerber zip archive.
