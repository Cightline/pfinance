clone this repository 

Put `t.py` in `~/.config/polybar`. 

Something like this should work: `ln -s /home/me/pfinance/t.py /home/me/.config/polybar/t.py`

Add this template to your `~/.config/polybar/config`

```
[module/TICKER]
type = custom/script
interval = 300
format = <label>
format-prefix = "TICKER: "
tail = true
format-prefix-foreground = ${colors.foreground-alt}
exec = ~/.config/polybar/t.py --ticker 'TICKER' --cp --down-color '%{F#bf0000}' --up-color '%{F#4b9653}'
```

Modify the template as you want. 
