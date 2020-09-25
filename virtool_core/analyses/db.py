async def remove_nuvs_blast(db, analysis_id, sequence_index):
    await db.analyses.update_one({"_id": analysis_id, "results.index": sequence_index}, {
        "$set": {
            "results.$.blast": None,
            "updated_at": virtool.utils.timestamp()
        }
    })
