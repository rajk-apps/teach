from teach.models import Course, CourseStructure, LectureStructure, SlideStructure


def get_content_occurrences(content):
    out = {}
    lss = [ls for s in content.slide_set.all() for ls in s.lecturestructure_set.all()]
    for ls in lss:
        lec = ls.lecture
        if lec.id in out.keys():
            out[lec.id]["slides"].append(ls)
        else:
            out[lec.id] = {"lec": lec, "slides": [ls]}
    return out.values()


def get_struct_dic(model, filter_kwargs, parent_model, subordernum=False):
    if subordernum:

        def sorter_fun(x):
            return (x.__getattribute__(parent_model).pk, x.ordernum, x.subordernum)

    else:

        def sorter_fun(x):
            return (x.__getattribute__(parent_model).pk, x.ordernum)

    all_structures = model.objects.filter(**filter_kwargs)
    out_dic = {}
    act_key = None
    for struct in sorted(all_structures, key=sorter_fun):
        parent_key = struct.__getattribute__(parent_model).pk
        if act_key == parent_key:
            out_dic[act_key].append(struct)
        else:
            act_key = parent_key
            out_dic[act_key] = [struct]
    return out_dic


def get_map_md(content_set):
    slide_structure_dic = get_struct_dic(
        SlideStructure, {"content__in": content_set}, "slide"
    )

    lecture_structure_dic = get_struct_dic(
        LectureStructure,
        {"slide__in": slide_structure_dic.keys()},
        "lecture",
        subordernum=True,
    )

    course_structure_dic = get_struct_dic(
        CourseStructure, {"lecture__in": lecture_structure_dic.keys()}, "course"
    )

    out_md = ""
    for cpk, css in course_structure_dic.items():
        course = Course.objects.get(pk=cpk)
        out_md += "\n- Course: {} ({})\n".format(course.name, cpk)
        for cs in css:
            lecture = cs.lecture
            out_md += "  - Lecture #{}: {} ({})\n".format(
                cs.ordernum, lecture.title, lecture.id
            )

            for ls in lecture_structure_dic[lecture.pk]:
                slide = ls.slide
                if ls.multislide:
                    ordernum = "{}/{}".format(ls.ordernum, ls.subordernum)
                else:
                    ordernum = ls.ordernum
                out_md += "    - Slide #{}: {} ({})\n".format(
                    ordernum, slide.title, slide.id
                )
                for ss in slide_structure_dic[slide.pk]:
                    content = ss.content
                    out_md += "      - [{}](#{}) ({})\n".format(
                        content.id, content.id, content.title
                    )
    return out_md
