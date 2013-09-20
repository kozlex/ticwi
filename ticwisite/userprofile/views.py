from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from forms import UserProfileForm, InstProfileForm
from django.contrib.auth.decorators import login_required



def redirect_to_desktop(request):
    if request.user.user_type == "i":  
        return HttpResponseRedirect('/userprofile/inst_profile')
    else:
        return HttpResponseRedirect('/userprofile/user_profile')

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/desktop')
    else:
        form = UserProfileForm()
        
    args = {}
    args.update(csrf(request))
    
    args['form'] = form
    
    return render_to_response('user_profile.html', args)   


def inst_profile(request):
    if request.method == 'POST':
        form = InstProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            a = form.save() 
 #(commit = False)
            #a.user  = request.user
            #a.save()
            return HttpResponseRedirect('/ticwiapp/desktop')
    else:
        form = InstProfileForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('inst_profile.html', args)

