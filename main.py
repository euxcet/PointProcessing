import click
from ui import UI
from picture import Picture



@click.command(help = 'Change luminance and contrast.')
@click.argument('image_path')
def lc(image_path):
	ui = UI()
	ui.load_img(image_path)
	ui.create_lumi_scale()
	ui.create_cont_scale()
	ui.start()


@click.command(help = "Histogram matching.")
@click.argument('image_path_1')
@click.argument('image_path_2', default = '')
def hm(image_path_1, image_path_2):
	if (image_path_2 == ''):
		ui = UI()
		ui.load_img(image_path_1, label = "source", row = 1, col = 0)
		ui.create_hm_single_buttons(row = 4, col = 1)
		ui.load_img(image_path_1, label = "result", row = 4, col = 0)
		ui.start()
	else:
		ui = UI()
		ui.load_img(image_path_1, label = "source", row = 1, col = 0)
		ui.load_img(image_path_2, label = "target", row = 1, col = 1)
		ui.create_hm_buttons(row = 4, col = 1)
		ui.load_img(image_path_1, label = "result", row = 4, col = 0)
		ui.start()


@click.command(help = "Histogram matching.(Background)")
@click.argument('image_path_1')
@click.argument('image_path_2', default = '')
def hmb(image_path_1, image_path_2):
	ui = UI()
	if (image_path_2 != ''):
		pic1 = Picture(image_path_1)
		pic2 = Picture(image_path_2)
		pic1.match_lumi(pic2)
		pic1.save("lumi_result.jpg")
		pic1 = Picture(image_path_1)
		pic1.match_rgb(pic2)
		pic1.save("rgb_result.jpg")
	else:
		pic1 = Picture(image_path_1)
		pic1.match_GB2R()
		pic1.save("GB2R.jpg")
		pic1 = Picture(image_path_1)
		pic1.match_RB2G()
		pic1.save("RB2G.jpg")
		pic1 = Picture(image_path_1)
		pic1.match_RG2B()
		pic1.save("RG2B.jpg")

@click.group()
def main():
	pass

main.add_command(lc)
main.add_command(hm)
main.add_command(hmb)

if __name__ == "__main__":
	main()
