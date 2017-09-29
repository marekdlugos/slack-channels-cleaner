function Channel(name, id, last_event, members)
{
    this.name = name;
    this.id = id;
    if (last_event != '-1')
        this.last_event = new Date(parseFloat(last_event) * 1000);
    else
        this.last_event = -1;
    this.members = parseInt(members);
}

Channel.prototype.toJSON = function() {
    return {'name': this.name, 'id': this.id};
}

function month_diff(from, to)
{
    var months = to.getMonth() - from.getMonth();
    var years = to.getFullYear() - from.getFullYear();
    return months + (12 * years);
}

function filter(channels, min_members, months)
{
    var filtered_channels = [];
    var today = new Date();

    for (var i = 0; i < channels.length; i++) {
        if (channels[i].members < min_members) {
            var le = channels[i].last_event;
            if (le == -1 || month_diff(le, today) >= months) {
                filtered_channels.push(channels[i]);
            }
        }
    }

    return filtered_channels;
}

function update_filtered(channels)
{
    $('#show_filtered').empty();

    var out = {'tofilter': []};
    for (var i = 0; i < channels.length; i++) {
        out['tofilter'].push(channels[i]);
        $('#show_filtered').append("<p>#" + channels[i].name + "</p>");
    }
    $('#hiddeninp').val(JSON.stringify(out));
    $('#number_of_channels').text(channels.length);
}
