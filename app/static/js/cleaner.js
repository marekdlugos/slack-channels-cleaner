function Channel(name, id, last_event, members)
{
    this.name = name;
    this.id = id;
    this.last_event = last_event;
    this.members = parseInt(members);
}

function filter(channels, min_members, months)
{
    var filtered_channels = [];

    for (var i = 0; i < channels.length; i++) {
        if (channels[i].members < min_members) {
            filtered_channels.push(channels[i]);
        }
    }

    return filtered_channels;
}

function update_filtered(channels)
{
    var selector = $('#filtered_channels');
    selector.empty();

    for (var i = 0; i < channels.length; i++) {
        var node = '<input type="hidden" name="' + channels[i].name + '" ' +
                   'value="' + channels[i].id + '">';
        selector.append(node);
    }
}
