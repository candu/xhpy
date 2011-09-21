def index(request):
  tags = Tag.objects.all()
  page = \
  <ui:page title="My Page">
    <ui:tags tags={tags} />
  <ui:page>
  # NOTE: the above tag has *not* been closed! Look carefully...
  return HttpResponse(page)
