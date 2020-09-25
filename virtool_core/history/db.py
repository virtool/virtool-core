


async def patch_to_version(app, otu_id: str, version: Union[str, int]) -> tuple:
    """
    Take a joined otu back in time to the passed ``version``. Uses the diffs in the change documents associated with
    the otu.

    :param app: the application object
    :param otu_id: the id of the otu to patch
    :param version: the version to patch to
    :return: the current joined otu, patched otu, and the ids of changes reverted in the process

    """
    db = app["db"]

    # A list of history_ids reverted to produce the patched entry.
    reverted_history_ids = list()

    current = await virtool.otus.db.join(db, otu_id) or dict()

    if "version" in current and current["version"] == version:
        return current, deepcopy(current), reverted_history_ids

    patched = deepcopy(current)

    # Sort the changes by descending timestamp.
    async for change in db.history.find({"otu.id": otu_id}, sort=[("otu.version", -1)]):
        if change["otu"]["version"] == "removed" or change["otu"]["version"] > version:
            reverted_history_ids.append(change["_id"])

            if change["diff"] == "file":
                change["diff"] = await virtool.history.utils.read_diff_file(
                    app["settings"]["data_path"],
                    otu_id,
                    change["otu"]["version"]
                )

            if change["method_name"] == "remove":
                patched = change["diff"]

            elif change["method_name"] == "create":
                patched = None

            else:
                diff = dictdiffer.swap(change["diff"])
                patched = dictdiffer.patch(diff, patched)
        else:
            break

    if current == {}:
        current = None

    return current, patched, reverted_history_ids